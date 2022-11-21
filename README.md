## CustomRSS

### Install

```bash
git clone git@github.com:finnito/customRSS.git
python3 -m venv ./venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

### Usage

Using this script is fairly simple. Use your browser inspector to get the requesite tags (see `feeds.config` for an example), and then run the script. It will output an `.xml` file for each feed as well as an `index.html` file that enumerates the feeds.

```bash
./main.py
```
