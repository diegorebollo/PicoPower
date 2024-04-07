# Autogenerated file
def render(wifi_list, ip, ping_interval, pin_relay, auto_turn_on):
    yield """
<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>PicoPower</title>
    <link rel=\"icon\" type=\"image/x-icon\" href=\"static/favicon.png\">
    <link rel=\"stylesheet\" href=\"static/mvp.css\" />
    <link rel=\"stylesheet\" href=\"static/custom.css\" />
  </head>
  <body>
    <header id=\"install-header\">
      <nav id=\"install-nav\">
        <a href=\"/\" id=\"name\">PicoPower</a>
        <ul>
          <li><a href=\"/install\">Settings</a></li>
        </ul>
      </nav>
    </header>
    <main>
      <section>
        <header>
          <h2>PicoPower Installation</h2>
        </header>
        <form method=\"post\">
          <label for=\"ssid\">Wifi SSID</label>
          <select id=\"ssid\" name=\"ssid\">
            """
    for ssid in (wifi_list):
        yield """
            <option value=\""""
        yield str(ssid)
        yield """\">"""
        yield str(ssid)
        yield """</option>
            """
    yield """
          </select>
          <label for=\"password\">Wifi Password</label>
          <input
            type=\"password\"
            id=\"password\"
            name=\"password\"
            size=\"30\"
            required
          />
          <label for=\"ip\">Device IP</label>
          <input type=\"text\" id=\"ip\" name=\"ip\" size=\"2\" value=\""""
    yield str(ip)
    yield """\" required />
          <label for=\"auto\">Auto Turn On</label>
          <select id=\"auto\" name=\"auto\">            
              <option value=\"True\">Enable</option>
              <option value=\"False\">Disable</option>            
          </select>
          <label for=\"time\">Ping Interval (minutes)</label>
          <input type=\"number\" id=\"time\" name=\"time\" size=\"2\" value=\""""
    yield str(ping_interval)
    yield """\" required />
          <label for=\"pin\">Relay Pin</label>
          <input type=\"number\" id=\"pin\" name=\"pin\" size=\"2\" value=\""""
    yield str(pin_relay)
    yield """\" required />
          <button type=\"submit\">Save</button>
        </form>
      </section>
    </main>
    <footer>
      <hr />
      <p>
        <small>© <a href=\"https://www.drebollo.com\">drebollo.com</a></small>
      </p>
    </footer>
  </body>
</html>
"""
