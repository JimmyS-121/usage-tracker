# AI Tool Usage Tracker

A Python-based tool to automatically track AI tool usage among staff, analyze usage data, and provide up-to-date recommendations—without requiring manual data uploads. The backend API collects usage data, performs analysis, and serves insights via a simple dashboard. The tool integrates with make.com for workflow automation and is designed for deployment on NorthFlank for scalable, sustainable hosting.

---

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Deployment](#deployment)
- [Integration with make.com](#integration-with-makecom)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- Automatic collection of AI tool usage data via API
- Storage of raw usage data in a database
- Periodic analysis with actionable recommendations
- RESTful API built with FastAPI
- Simple dashboard for visualization (optional frontend)
- Workflow automation via make.com scenarios
- Dockerized for easy deployment on NorthFlank

---

## Getting Started

### Prerequisites

- Python 3.11+
- Docker (for containerized deployment)
- NorthFlank account (for hosting)
- make.com account (for automation workflows)

### Installation

1. Clone the repository:

