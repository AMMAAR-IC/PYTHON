def naive_bayes_predict(weather):
    # Training data counts
    total = 14
    play_yes = 9
    play_no = 5

    # Likelihoods
    P_sunny_given_yes = 2 / 9
    P_sunny_given_no = 3 / 5

    # Priors
    P_yes = play_yes / total
    P_no = play_no / total

    # Naive Bayes formula (no denominator, we only compare)
    prob_yes = P_sunny_given_yes * P_yes
    prob_no = P_sunny_given_no * P_no

    # Prediction
    if prob_yes > prob_no:
        return "Play = Yes"
    else:
        return "Play = No"

# Predict for 'Sunny'
print("Prediction for Weather = Sunny:", naive_bayes_predict("Sunny"))
