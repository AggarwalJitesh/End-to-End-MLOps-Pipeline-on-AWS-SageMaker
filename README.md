# End-to-End-MLOps-Pipeline-on-AWS-SageMaker
A cloud-native ML pipeline that automatically ingests, processes, trains, deploys, and monitors a model.

We are building a production-grade MLOps pipeline on AWS.
That means:
1. Taking raw data → cleaning & transforming it into ML-ready format.
2. Training a model in the cloud on that data.
3. Deploying the model as a scalable API endpoint.
4. Integrating it into an application (via Lambda + API Gateway).
5. Monitoring its performance and health with CloudWatch.

 As a MLOps engineers and cloud solution architects do i am productionize AI so it’s reliable, repeatable, and scalab

 # Titanic Survival Prediction with AWS SageMaker
This project predicts Titanic passenger survival using AWS SageMaker.

Tech Stack : Why We Choose them

1. S3 : Storage for raw datasets, processed training data, and model artifacts.
2. Glue : Serverless ETL (Extract–Transform–Load). Cleans data, fills missing values, encodes categories, outputs ML-ready CSV.
3. SageMaker (Training) : Managed ML training service. Runs XGBoost model on your preprocessed Titanic data.
4. SageMaker (Endpoint) : Hosting service for trained models. Gives you a real-time API to make predictions.
5. Lambda : Lightweight serverless compute. Used to call the SageMaker endpoint and add business logic (e.g., classify survived=1 vs not).
6. API Gateway : Exposes your Lambda function as a secure REST API.
7. CloudWatch : Monitoring service. Tracks inference latency, errors, usage, and sends alerts.


So the pipeline flow is: 
#### Raw data (S3) → Cleaning (Glue) → Training (SageMaker) → Model (S3 artifact) → Endpoint (SageMaker) → Access via Lambda + API Gateway → Monitoring (CloudWatch)


**1. Download Raw Data (Kaggle → Local → S3)**
I started with the Titanic dataset from Kaggle. The raw CSV was uploaded to an Amazon S3 bucket, which serves as the central storage for all raw and processed data files.
<img width="1439" height="769" alt="1" src="https://github.com/user-attachments/assets/20124d7a-f719-40c1-b202-0309a185fb74" />


**2. S3 – Data Lake**
Amazon S3 acted as the data lake for the project. It stored:

* Raw Titanic dataset (uploaded manually)
* Processed training/validation datasets (from Glue jobs)
* Model artifacts (generated after SageMaker training)

**3. Glue – Data Preprocessing**
Using AWS Glue (serverless ETL), I automated the preprocessing pipeline:

* Removed irrelevant columns
* Filled missing values (mean/median for numerics, mode for categoricals)
* Encoded categorical features (e.g., gender, class)
* Saved cleaned dataset back into S3
* IAM role: Glue service role with access to your S3 buckets
<img width="1439" height="769" alt="1 5" src="https://github.com/user-attachments/assets/d19c0575-034b-461e-a325-4e5b3767227d" />
<img width="1439" height="769" alt="1 8" src="https://github.com/user-attachments/assets/1d33fcc5-bb66-4cce-8f36-355b7c942e2f" />
<img width="1439" height="769" alt="2 5" src="https://github.com/user-attachments/assets/fc767cae-9d8c-4f17-8efe-5757cf4aa6d7" />
<img width="1439" height="769" alt="3" src="https://github.com/user-attachments/assets/72bfda5c-19a0-4277-b1f6-b6868a9d5f35" />

**4. SageMaker (Training Job)**
I trained an **XGBoost classifier** in SageMaker. The Glue-processed dataset was used to fit the model. SageMaker handled compute resources, scaling, and produced model artifacts in S3.
**Input data channels:**

* **train**: S3 URI → s3://mlops-titanic-processed/train/
* **validation**: S3 URI → s3://mlops-titanic-processed/validation/
* Content type: text/csv

**Output path:**

* s3://mlops-titanic-artifacts/xgb-output/

**Resource config:**

* Instance type: ml.m5.large
* Volume: 10 GB
* Max runtime: 3600s

**Hyperparameters (good starters):**

* objective: binary:logistic
* num_round: 200
* max_depth: 5
* eta: 0.2
* subsample: 0.8
* eval_metric: auc
* verbosity: 1

**IAM role:** create **AmazonSageMaker-ExecutionRole** with S3 access.
<img width="1439" height="769" alt="4" src="https://github.com/user-attachments/assets/c3167c58-bfe8-4474-852f-ff2f6d67f47e" />
<img width="1439" height="769" alt="5" src="https://github.com/user-attachments/assets/97b3b116-f229-4fc5-845f-52cfb8abe5f5" />
<img width="1439" height="769" alt="8" src="https://github.com/user-attachments/assets/0e437c34-5bf8-465e-9903-0db6a0c9074c" />
<img width="1439" height="769" alt="9" src="https://github.com/user-attachments/assets/fb74279b-d969-4aa0-a247-a2cf78e1e937" />
<img width="1439" height="769" alt="11" src="https://github.com/user-attachments/assets/58956288-fb75-4cfb-b11c-0ed54e9ab7e2" />
<img width="1439" height="769" alt="11 5" src="https://github.com/user-attachments/assets/027af13a-92aa-4b9c-8fa7-cdf397afb776" />
<img width="1439" height="769" alt="12" src="https://github.com/user-attachments/assets/42c29d96-48bf-4462-981c-d6bf305f5ab0" />


**5. SageMaker (Create Model & Endpoint Deployment)**

From the completed training job page:
**Actions → Create model**
* Model name: titanic-xgb-model

Then **Deploy**:

* **Create endpoint** (it will auto-create endpoint config)
The trained model was deployed as a **real-time inference endpoint** in SageMaker. The endpoint provides an API-style interface to send passenger data and receive survival predictions.

<img width="1439" height="769" alt="13" src="https://github.com/user-attachments/assets/77c126fa-a3e5-4e9b-9f91-34e5ddd0bd74" />
<img width="1439" height="769" alt="14" src="https://github.com/user-attachments/assets/a1e9e783-c9e9-48b5-b914-bbde96723052" />
<img width="1439" height="769" alt="15" src="https://github.com/user-attachments/assets/aa0288c3-6011-485a-8084-0d3d5b6c6870" />
<img width="1439" height="769" alt="16" src="https://github.com/user-attachments/assets/0fc5e172-4ec9-4c29-92c4-492b6bac7a4f" />



**6. AWS Lambda – Business Logic Layer**
I created a Lambda function to interact with the SageMaker endpoint. It sends requests, receives predictions, and applies simple business logic (e.g., converting model output into “Survived” or “Not Survived”).
Role: create new or use one with sagemaker:InvokeEndpoint
<img width="1439" height="769" alt="16 5" src="https://github.com/user-attachments/assets/ba380773-9767-46e3-8768-f89dd92a5ad9" />
<img width="1439" height="769" alt="17" src="https://github.com/user-attachments/assets/877e92e9-4a7e-4d76-9122-d5abdfa40203" />
<img width="1439" height="769" alt="18" src="https://github.com/user-attachments/assets/2a165083-270f-4043-bf11-e80513dde8be" />
<img width="1439" height="769" alt="19" src="https://github.com/user-attachments/assets/36748559-7183-4d6a-a96a-53e80346a032" />


**7. API Gateway – Public REST API**
Using API Gateway, I exposed the Lambda function as a secure REST API. This allowed external clients to make HTTP requests and get predictions without direct access to SageMaker.
<img width="1439" height="769" alt="19 5" src="https://github.com/user-attachments/assets/ea888321-55ea-44c1-86b9-b66f7933e840" />
<img width="1439" height="769" alt="20" src="https://github.com/user-attachments/assets/f8793019-994c-4b2b-9d9b-f4a89c0e58b7" />


**8. CloudWatch – Monitoring & Logs**
CloudWatch tracked:

* Inference latency & error rates
* Lambda execution logs
* Endpoint invocation metrics
<img width="1439" height="769" alt="21" src="https://github.com/user-attachments/assets/2cf1cbd2-6c52-4c54-9bd9-b9c91e95462c" />
<img width="1439" height="769" alt="22" src="https://github.com/user-attachments/assets/4581de2f-ac8d-4024-9095-bf6fe00fc245" />
<img width="1439" height="769" alt="23" src="https://github.com/user-attachments/assets/b811917d-92a8-41e5-a747-fc17731c596f" />
<img width="1439" height="769" alt="24" src="https://github.com/user-attachments/assets/8e96672a-04dd-44d0-ab2c-8b471d37a46b" />


I also configured short log retention to avoid unnecessary AWS charges.

**9. Cleanup (Cost Optimization)**
To prevent ongoing charges, I deleted:

* SageMaker endpoints, models, configs
* Glue jobs/crawlers
* API Gateway & Lambda (demo use case)
* CloudWatch log groups


