from invest_assistant.analytics import log_returns
import pandas as pd

def test_log_returns_shape():
    df = pd.DataFrame({"A":[100,110,121]})
    r = log_returns(df)
    assert r.shape == (2,1)
