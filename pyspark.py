import sys, boto3
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, DoubleType

spark = SparkSession.builder.getOrCreate()

# ---- CONFIG ----
RAW_S3 = "s3://mlops-titanic-<you>-raw/raw/train.csv"
OUT_S3 = "s3://mlops-titanic-<you>-processed/"
TRAIN_PATH = OUT_S3 + "train/train.csv"
VAL_PATH = OUT_S3 + "validation/validation.csv"
SPLIT_TRAIN = 0.8

# ---- LOAD ----
df = spark.read.csv(RAW_S3, header=True, inferSchema=True)

# ---- CLEAN/SELECT ----
df = df.select(
    "Survived","Pclass","Sex","Age","SibSp","Parch","Fare","Embarked"
)

# Impute missing numeric
for c in ["Age", "Fare"]:
    median_val = df.approxQuantile(c, [0.5], 0.25)[0]
    df = df.fillna({c: float(median_val)})

# Encode 'Sex'
df = df.withColumn("Sex",
    F.when(F.col("Sex")=="male", F.lit(1)).otherwise(F.lit(0)).cast(IntegerType())
)

# Encode 'Embarked'
df = df.fillna({"Embarked": "S"})
df = df.withColumn("Embarked",
    F.when(F.col("Embarked")=="S", F.lit(0))
     .when(F.col("Embarked")=="C", F.lit(1))
     .otherwise(F.lit(2)).cast(IntegerType())
)

# Cast numerics
for c in ["Pclass","Age","SibSp","Parch","Fare"]:
    df = df.withColumn(c, F.col(c).cast(DoubleType()))

# Order: label first (XGBoost on SageMaker prefers label first, no header)
cols = ["Survived","Pclass","Sex","Age","SibSp","Parch","Fare","Embarked"]
df = df.select(*cols)

# Split
train_df, val_df = df.randomSplit([SPLIT_TRAIN, 1.0-SPLIT_TRAIN], seed=42)

# Write CSV without header
(train_df.coalesce(1)
 .write.mode("overwrite").option("header","false").csv(TRAIN_PATH))
(val_df.coalesce(1)
 .write.mode("overwrite").option("header","false").csv(VAL_PATH))
