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

