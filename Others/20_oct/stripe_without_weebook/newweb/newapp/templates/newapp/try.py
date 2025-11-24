import stripe
charge = stripe.Charge.retrieve(
  "ch_3LvHfq2eZvKYlo2C1V25irio",
  api_key="sk_test_51LsfxwSFADRI1Ttj0Q0BiO8S6iqXGKJnA2NPdc5IBa9oRaJPjoJdisKx3Whn6tp8QVY72PKcSMsdA5L9MpkYUIEn00SQPbtbNh"
)
charge.save() # Uses the same API Key.