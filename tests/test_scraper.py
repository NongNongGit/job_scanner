from job_scanner.linkedin_scraper import fetch_linkedin_jobs, normalize


def test_normalize_list():
    assert normalize(["A", "B"]) == "A, B"


def test_normalize_none():
    assert normalize(None) == ""


def test_scraper_normalization(monkeypatch):
    def fake_get(url, headers, params):
        class FakeResponse:
            def json(self):
                return {
                    "data": [
                        {
                            "title": ["Software Engineer"],
                            "company": ["Microsoft", "NZ"],
                            "location": ["Auckland"],
                            "salary": 100000,
                            "url": "http://example.com",
                            "description": ["Great job"],
                        }
                    ]
                }

        return FakeResponse()

    monkeypatch.setattr("requests.get", fake_get)

    profile = {
        "linkedin": {
            "keywords": ["Software Engineer"],
            "location": "Auckland",
            "job_types": ["full-time"],
            "max_results": 10,
        }
    }

    jobs = fetch_linkedin_jobs(profile)

    assert len(jobs) == 1
    job = jobs[0]

    assert job["title"] == "Software Engineer"
    assert job["company"] == "Microsoft, NZ"
    assert job["location"] == "Auckland"
    assert job["salary"] == 100000
