# GitHub Trending

A Python package that allows you to fetch trending repositories from GitHub. This tool scrapes the GitHub trending page and provides structured data about trending repositories.

## Features

- Fetch trending repositories from GitHub
- Filter by date (daily, weekly, monthly)
- Get repository details including:
  - Repository name
  - Link
  - Description
  - Programming language
  - Star count

## Installation

This project uses Python 3.13 or higher. Make sure you have Python installed.

1. Clone the repository:
```bash
git clone https://github.com/leodo9x/github-trending.git
cd github-trending
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
github-trending/
├── app/
│   ├── main.py           # FastAPI application and routes
│   └── github_trending.py # Core functionality for fetching trending repos
├── tests/                # Test files
├── requirements.txt      # Python dependencies
└── vercel.json          # Vercel deployment configuration
```

## Usage

### Python Package

Here's a simple example of how to use the package:

```python
from app.github_trending import init

# Get today's trending repositories
trending_repos = init()

# Get weekly trending repositories
weekly_trending = init(date='weekly')

# Get monthly trending repositories
monthly_trending = init(date='monthly')

# Print repository information
for repo in trending_repos:
    print(f"Name: {repo['name']}")
    print(f"Link: {repo['link']}")
    print(f"Description: {repo['description']}")
    print(f"Language: {repo['language']}")
    print(f"Stars: {repo['star']}")
    print("---")
```

### API Endpoint

The package provides a FastAPI endpoint to fetch trending repositories:

```bash
# Get today's trending repositories
curl http://localhost:8000/api/github-trending

# Get weekly trending repositories
curl http://localhost:8000/api/github-trending?since=weekly

# Get monthly trending repositories
curl http://localhost:8000/api/github-trending?since=monthly
```

The API returns data in the following format:
```json
{
  "code": 200,
  "data": [
    {
      "name": "repository-name",
      "link": "github.com/username/repository",
      "description": "Repository description",
      "language": "Programming language",
      "star": "Number of stars"
    }
  ]
}
```

## Development

To run the development server:

```bash
uvicorn app.main:app --reload
```

## Deployment

### Deploying to Vercel

1. Install the Vercel CLI:
```bash
npm install -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy the application:
```bash
vercel
```

4. For production deployment:
```bash
vercel --prod
```

The application will be deployed to Vercel and you'll receive a URL where your API is accessible.

## Dependencies

- Python >= 3.13
- requests >= 2.32.3
- beautifulsoup4 >= 4.13.4
- fastapi >= 0.109.0
- uvicorn >= 0.27.0
- mangum >= 0.17.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
