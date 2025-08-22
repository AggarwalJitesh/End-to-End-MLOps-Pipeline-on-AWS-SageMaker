import os, json, boto3

ENDPOINT_NAME = os.environ.get("ENDPOINT_NAME", "titanic-xgb-endpoint")
smrt = boto3.client("sagemaker-runtime")

# Feature order: Pclass, Sex, Age, SibSp, Parch, Fare, Embarked
# CSV row must NOT include header; label is unknown at inference
def lambda_handler(event, context):
    features = event.get("features")
    # Example features if none provided (3rd class female, age 26, no siblings/parents, fare 7.9, embarked S)
    if not features:
        features = [3, 0, 26.0, 0, 0, 7.9, 0]

    payload = ",".join(str(x) for x in features)  # no label at inference
    resp = smrt.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType="text/csv",
        Body=payload
    )
    body = resp["Body"].read().decode("utf-8")
    # XGBoost outputs probability for binary:logistic
    prob = float(body.strip())
    pred = 1 if prob >= 0.5 else 0
    return {
        "prediction": pred,
        "probability_survived": prob,
        "features": features
    }
