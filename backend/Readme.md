# Garage CRUD REST API

## Overview

The Garage CRUD REST API is a project that provides endpoints for managing a garage, allowing users to perform basic CRUD operations (Create, Read, Update, Delete) on garage items. The API is designed to be used for managing a collection of items stored in a garage, such as cars, tools, or other equipment.

## Features

- **Create:** Add new items to the garage (Not implemented yet).
- **Read:** Retrieve information about items in the garage.
- **Update:** Modify the details of existing items.
- **Delete:** Remove items from the garage.

## API Endpoints

### 1. Read (GET)

- **Get All Items:**
  - Endpoint: `/api/items`
  - Description: Retrieve a list of all items in the garage.

- **Get Item by ID:**
  - Endpoint: `/api/items/{id}`
  - Description: Retrieve details of a specific item by its ID.

### 2. Create (POST) - Not Implemented

- **Add New Item:**
  - Endpoint: `/api/items`
  - Description: (Not implemented yet) Add a new item to the garage.

### 3. Update (PUT)

- **Update Item by ID:**
  - Endpoint: `/api/items/{id}`
  - Description: Update the details of a specific item in the garage.

### 4. Delete (DELETE)

- **Delete Item by ID:**
  - Endpoint: `/api/items/{id}`
  - Description: Remove a specific item from the garage.

## Getting Started

### Prerequisites
    pip freeze > requirements.txt

    