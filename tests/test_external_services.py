def test_remote_service_health(ssh_client):
    uptime = ssh_client.execute("uptime")
    assert "load average" in uptime
