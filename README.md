# GCP Setup

NOTE: overlap between:

* <https://console.cloud.google.com/home/dashboard>
* <https://console.firebase.google.com>

## 1. Install GCP cli locally - Ubuntu 20.04

```bash
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] \
    https://packages.cloud.google.com/apt cloud-sdk main" \
    | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

sudo apt install apt-transport-https ca-certificates gnupg

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg \
    | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

sudo apt update && sudo apt install google-cloud-sdk

gcloud init

# login via Web UI & create env - https://console.cloud.google.com/home/dashboard

# use us_central1 - as it's part of free usage
```

---

## 2. In GCP dashboard

* create Project

### 2.1. Create Firestore instance

* Create Firestore
  * Native mode instance
  * eur3 (multi region)
  * favourites_collection
  
### 2.2. Create Service Account

* create Service Account with roles:
  * Cloud Functions Admin
  * Firebase Admin SDK Administrator Service Agent
  * Service Account Token Creator
  * Service Account User
  * Logs Writer
* export JSON key of Service Account

## 3. In cli, for project, do one off tasks

```text
gcloud init

gcloud services enable cloudfunctions.googleapis.com

gcloud services enable cloudbuild.googleapis.com

gcloud services enable logging.googleapis.com
```

---

## 4. GitHub Secret - GOOGLE_APPLICATION_CREDENTIALS

* base64 config/dev-service-account.json

## 5. Test

### 5.1. pycharm

* run 'pytest gcp dev'

### 5.2. curl - localhost + Firestore in GCP

```text
export GOOGLE_APPLICATION_CREDENTIALS=config/dev-service-account.json

curl -X POST \
  http://127.0.0.1:5000/save \
  -H "Content-Type:application/json" \
  -d '{"code": "qski!$£90d", "digests": ["1", "2"]}'
  
  
curl -X POST \
  http://127.0.0.1:5000/receive \
  -H "Content-Type:application/json" \
  -d '{"code": "qski!$£90d"}'
```
