# Deploying to Vercel

This guide explains how to deploy your Flask Real Estate application to Vercel.

## Prerequisites

1.  **Vercel Account**: Create one at [vercel.com](https://vercel.com).
2.  **Vercel CLI** (Optional): Install via `npm i -g vercel`.
3.  **PostgreSQL Database**: Since Vercel is serverless, you cannot use the local SQLite database. You need a hosted PostgreSQL database.
    - **Option A**: Use [Vercel Postgres](https://vercel.com/docs/storage/vercel-postgres).
    - **Option B**: Use [Supabase](https://supabase.com/).
    - **Option C**: Use [Render PostgreSQL](https://render.com/).

## Step 1: Prepare the Database

1.  Create a new PostgreSQL database on your chosen provider.
2.  Get the **Connection String** (URL). It usually looks like:
    `postgresql://user:password@host:port/database_name`

## Step 2: Deploy

### Option A: Using Vercel CLI (Recommended for first time)

1.  Open your terminal in this project directory.
2.  Run the deploy command:
    ```bash
    npx vercel
    ```
3.  Follow the prompts:

    - Set up and deploy? **Y**
    - Which scope? (Select your account)
    - Link to existing project? **N**
    - Project name? (Press Enter or type a name)
    - In which directory is your code located? **./** (Press Enter)
    - Want to modify these settings? **N**

4.  **Wait for the build to fail or complete.** It might fail initially because environment variables are missing.

### Option B: Using GitHub

1.  Push this code to a GitHub repository.
2.  Go to your Vercel Dashboard and click **"Add New..."** -> **"Project"**.
3.  Import your GitHub repository.

## Step 3: Configure Environment Variables

1.  Go to your project settings on Vercel: **Settings** -> **Environment Variables**.
2.  Add the following variables:

# Deploying to Vercel

This guide explains how to deploy your Flask Real Estate application to Vercel.

## Prerequisites

1.  **Vercel Account**: Create one at [vercel.com](https://vercel.com).
2.  **Vercel CLI** (Optional): Install via `npm i -g vercel`.
3.  **PostgreSQL Database**: Since Vercel is serverless, you cannot use the local SQLite database. You need a hosted PostgreSQL database.
    - **Option A**: Use [Vercel Postgres](https://vercel.com/docs/storage/vercel-postgres).
    - **Option B**: Use [Supabase](https://supabase.com/).
    - **Option C**: Use [Render PostgreSQL](https://render.com/).

## Step 1: Prepare the Database

1.  Create a new PostgreSQL database on your chosen provider.
2.  Get the **Connection String** (URL). It usually looks like:
    `postgresql://user:password@host:port/database_name`

## Step 2: Deploy

### Option A: Using Vercel CLI (Recommended for first time)

1.  Open your terminal in this project directory.
2.  Run the deploy command:
    ```bash
    vercel
    ```
3.  Follow the prompts:

    - Set up and deploy? **Y**
    - Which scope? (Select your account)
    - Link to existing project? **N**
    - Project name? (Press Enter or type a name)
    - In which directory is your code located? **./** (Press Enter)
    - Want to modify these settings? **N**

4.  **Wait for the build to fail or complete.** It might fail initially because environment variables are missing.

### Option B: Using GitHub

1.  Push this code to a GitHub repository.
2.  Go to your Vercel Dashboard and click **"Add New..."** -> **"Project"**.
3.  Import your GitHub repository.

## Step 3: Configure Environment Variables

1.  Go to your project settings on Vercel: **Settings** -> **Environment Variables**.
2.  Add the following variables:

    | Key                     | Value               | Description                                                                 |
    | :---------------------- | :------------------ | :-------------------------------------------------------------------------- |
    | `DATABASE_URL`          | `postgresql://...`  | Your database connection string.                                            |
    | `SECRET_KEY`            | `your-secret-key`   | A long random string for security.                                          |
    | `ADMIN_USERNAME`        | `admin`             | Username for the admin panel.                                               |
    | `ADMIN_PASSWORD`        | `secure_password`   | Password for the admin panel.                                               |
    | `MAIL_USERNAME`         | `your@email.com`    | (Optional) For sending emails.                                              |
    | `MAIL_PASSWORD`         | `your-app-password` | (Optional) App password for email.                                          |
    | `BLOB_READ_WRITE_TOKEN` | `...`               | Token for Vercel Blob storage (automatically added if you use Vercel Blob). |

3.  **Redeploy** your application for the changes to take effect.
    - CLI: `npx vercel --prod`
    - GitHub: Push a new commit or redeploy from the dashboard.

## Important Limitations

### 1. File Uploads

- **Vercel Blob**: The application is now configured to use Vercel Blob for file uploads if `BLOB_READ_WRITE_TOKEN` is present.
- **Setup**: Go to Vercel Dashboard -> Storage -> Create Database -> Blob. Connect it to your project. This will automatically add the `BLOB_READ_WRITE_TOKEN`.
- **Fallback**: If Blob is not configured, it will try to save to the local filesystem, which **will not persist**.

### 2. Database

- The application is configured to automatically switch to PostgreSQL if `DATABASE_URL` is present.
- Ensure you run the database migrations or let `db.create_all()` run (which happens in `app.py` on startup if tables don't exist).
