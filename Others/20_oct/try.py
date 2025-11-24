import cgi

requestParams = {
'command' : 'AUTHORIZATION',
'access_code' : 'zx0IPmPy5jp1vAz8Kpg7',
'merchant_identifier' : 'CycHZxVj',
'merchant_reference' : 'XYZ9239-yu898',
'amount' : '10000',
'currency' : 'AED',
'language' : 'en',
'customer_email' : 'test@payfort.com',
'signature' : '7cad05f0212ed933c9a5d5dffa31661acf2c827a',
'order_description' : 'iPhone 6-S',
}


redirectUrl = 'https://sbcheckout.payfort.com/FortAPI/paymentPage';
print ("<html xmlns='https://www.w3.org/1999/xhtml'>\n<head></head>\n<body>\n")
print ("<form action='redirectUrl' method='post' name='frm'>\n")
for slug, title in requestParams.items():
    print( "\t<input type='hidden' name='"+ slug+"' value='"+ title+"'>\n")

print ("</form>")
print ("\t<script type='text/javascript'>\n")
print ("\t\tdocument.frm.submit();\n")
print ("\t</script>\n")
print ("\n</body>\n</html>")