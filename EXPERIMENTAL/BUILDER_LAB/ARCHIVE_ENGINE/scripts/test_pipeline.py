from ENGINE.nexah_engine import run_engine


def test_pipeline():

    print("\nRunning NEXAH pipeline test\n")

    results = run_engine()

    assert "architecture" in results
    assert "graph" in results
    assert "resilience" in results
    assert "landscape" in results
    assert "transitions" in results
    assert "navigation" in results

    print("\nPipeline test successful\n")


if __name__ == "__main__":
    test_pipeline()
