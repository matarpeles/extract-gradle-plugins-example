
# Gradle Plugin and Service Updater for Port

## Overview

This repository contains a **GitHub Actions workflow** and supporting Python script to:
- Extract **plugins** and their **versions** from a Gradle build file.
- Map the extracted plugins as **package entities** in Port.
- Automatically create or update a **service entity** in Port, connecting it to its plugin dependencies.

This workflow simplifies tracking dependencies for your services by automating the extraction and ingestion of Gradle plugin data into Port.

---

## Getting Started

### 1. Saving Port Credentials as Repository Secrets

To authenticate with Port, you need to save your credentials as **repository secrets** in GitHub:

1. Navigate to your GitHub repository.
2. Go to **Settings** > **Secrets and variables** > **Actions** > **New repository secret**.
3. Add the following secrets:
   - **`CLIENT_ID`**: Your Port client ID.
   - **`CLIENT_SECRET`**: Your Port client secret.

---

### 2. Creating the Blueprints

Before running the workflow, ensure that the required **blueprints** are created in Port.

#### a) Creating the Service Blueprint

The **Service** blueprint represents your service and its relationships to dependencies. Use the following JSON to create the blueprint in Port:

\`\`\`json
{
  "identifier": "service",
  "title": "Service",
  "icon": "Github",
  "schema": {
    "properties": {
      "readme": {
        "title": "README",
        "type": "string",
        "format": "markdown",
        "icon": "Book"
      },
      "url": {
        "title": "URL",
        "format": "url",
        "type": "string",
        "icon": "Link"
      },
      "language": {
        "type": "string",
        "title": "Language",
        "icon": "Git"
      },
      "slack": {
        "icon": "Slack",
        "type": "string",
        "title": "Slack",
        "format": "url"
      },
      "tier": {
        "title": "Tier",
        "type": "string",
        "description": "How mission-critical the service is",
        "enum": [
          "Mission Critical",
          "Customer Facing",
          "Internal Service",
          "Other"
        ],
        "enumColors": {
          "Mission Critical": "turquoise",
          "Customer Facing": "green",
          "Internal Service": "darkGray",
          "Other": "yellow"
        },
        "icon": "DefaultProperty"
      },
      "gradle_file": {
        "type": "string",
        "title": "Gradle file"
      }
    },
    "required": []
  },
  "mirrorProperties": {},
  "calculationProperties": {},
  "aggregationProperties": {},
  "relations": {
    "dependencies": {
      "title": "Dependencies",
      "target": "package",
      "required": false,
      "many": true
    }
  }
}
\`\`\`

---

#### b) Creating the Package Blueprint

The **Package** blueprint represents each plugin as a dependency. Use the following JSON to create the blueprint in Port:

\`\`\`json
{
  "identifier": "package",
  "title": "Package",
  "icon": "Package",
  "schema": {
    "properties": {
      "package": {
        "icon": "DefaultProperty",
        "type": "string",
        "title": "Package"
      },
      "version": {
        "icon": "DefaultProperty",
        "type": "string",
        "title": "Version"
      }
    },
    "required": [
      "package",
      "version"
    ]
  },
  "mirrorProperties": {},
  "calculationProperties": {},
  "aggregationProperties": {},
  "relations": {}
}
\`\`\`

---

### 3. Running the Workflow

Once the blueprints are set up and your Port credentials are saved as secrets, you’re ready to run the workflow.

#### Steps:

1. Navigate to the **Actions** tab in your GitHub repository.
2. Select the **"Extract and Upsert Gradle Plugins and Service to Port"** workflow.
3. Click **Run workflow** and provide the following input:
   - **`gradle_path`**: The path to the Gradle build file. Default: `./build.gradle`.

The workflow will:
- Parse the specified Gradle file.
- Extract plugins and their versions.
- Upsert the `service` and `package` entities into Port, linking the service to its dependencies.

---

## Example Gradle File

Here’s an example Gradle file to test the workflow:

\`\`\`gradle
plugins {
    id 'org.springframework.boot' version '3.1.2'
    id 'com.github.spotbugs' version '5.0.13'
}

repositories {
    mavenCentral()
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter'
    testImplementation 'org.junit.jupiter:junit-jupiter'
}
\`\`\`

---

## Output Example

After the workflow runs, you’ll see:

1. A **service entity** in Port, named after your GitHub repository (e.g., `my-repo`), with a relation to:
2. **Package entities** for each Gradle plugin extracted from the build file.

This integration helps you track dependencies for your services efficiently.
