import pandas as pd


pd.read_csv("data\kalshi_panel.csv")



sbr_nrc = '''You are an expert superforecaster, familiar with the work of Philip Tetlock.

Question: {question}
Possible outcomes: Yes (1) or No (0)
Resolution criteria: {rules}
Scheduled close date: {expiration_time}
(Note: The question may resolve before this date.)

Instructions:
Please provide a single best estimate of the base rate for the event occurring.

Output your answer as a valid JSON object with exactly the following fields:
- "reasoning": A brief explanation of how the base rate estimate was derived.
- "base_rate": A single numeric value between 0 and 1, inclusive.

Your final output must be a JSON object and must include no other text outside of the JSON.
'''

mbr_nrc = '''
You are an expert superforecaster, familiar with the work of Philip Tetlock.

Question: {question}
Possible outcomes: Yes (1) or No (0)
Resolution criteria: {rules}
Scheduled close date: {expiration_time}
(Note: The question may resolve before this date.)

Instructions:
Please provide multiple strong candidate estimates of the base rate for the event occurring.

Output your answer as a valid JSON object with exactly the following fields:
- "reasoning": A brief explanation of how the base rate estimates were derived.
- "base_rates": An array of numeric values between 0 and 1, inclusive.

Your final output must be a JSON object and must include no other text outside of the JSON.
'''
cbr_nrc = '''
You are an expert superforecaster, familiar with the work of Philip Tetlock.

Question: {question}
Possible outcomes: Yes (1) or No (0)
Resolution criteria: {rules}
Scheduled close date: {expiration_time}
(Note: The question may resolve before this date.)

Instructions:
1. Please provide multiple strong candidate estimates of the base rate for the event occurring.
2. Compare and evaluate the different base rate estimates, and select the one you judge to be most appropriate and useful for this forecasting task.

Output your answer as a valid JSON object with exactly the following fields:
- "reasoning": A brief explanation of how the base rate estimates were derived and evaluated.
- "base_rates": An array of numeric values between 0 and 1, inclusive.
- "selected_base_rate": A single numeric value between 0 and 1, inclusive.

Your final output must be a JSON object and must include no other text outside of the JSON.
'''
sbr_src  = '''You are an expert superforecaster, familiar with the work of Philip Tetlock.

Question: {question}
Possible outcomes: Yes (1) or No (0)
Resolution criteria: {rules}
Scheduled close date: {expiration_time}
(Note: The question may resolve before this date.)

Instructions:
1. Identify a single best reference class that would be most appropriate for generating base rates for this question.
2. For this reference class, please provide a single best estimate of the base rate for the event within this reference class.

Output your answer as a valid JSON object with exactly the following fields:
- "reasoning": A brief explanation of how the reference class and the base rate estimate were derived.
- "reference_class": A clear and concise description of the chosen reference class.
- "base_rate": A single numeric value between 0 and 1, inclusive.

Your final output must be a JSON object and must include no other text outside of the JSON.
'''
mbr_src = '''
You are an expert superforecaster, familiar with the work of Philip Tetlock.

Question: {question}
Possible outcomes: Yes (1) or No (0)
Resolution criteria: {rules}
Scheduled close date: {expiration_time}
(Note: The question may resolve before this date.)

Instructions:
1. Identify a single best reference class that would be most appropriate for generating base rates for this question.
2. For this reference class, please provide multiple strong candidate estimates of the base rate for the event within this reference class.

Output your answer as a valid JSON object with exactly the following fields:
- "reasoning": A brief explanation of how the reference class and the base rate estimates were derived.
- "reference_class": A clear and concise description of the chosen reference class.
- "base_rates": An array of numeric values between 0 and 1, inclusive.

Your final output must be a JSON object and must include no other text outside of the JSON.
'''
cbr_src = '''You are an expert superforecaster, familiar with the work of Philip Tetlock.

Question: {question}
Possible outcomes: Yes (1) or No (0)
Resolution criteria: {rules}
Scheduled close date: {expiration_time}
(Note: The question may resolve before this date.)

Instructions:
1. Identify a single best reference class that would be most appropriate for generating base rates for this question.
2. For this reference class, please provide multiple strong candidate estimates of the base rate for the event within this reference class.
3. Compare and evaluate the different base rate estimates, and select the one you judge to be most appropriate and useful for this forecasting task.


Output your answer as a valid JSON object with exactly the following fields:
- "reasoning": A brief explanation of how the reference class and the base rate estimates were derived and evaluated.
- "reference_class": A clear and concise description of the chosen reference class.
- "base_rates": An array of numeric values between 0 and 1, inclusive.
- "selected_base_rate": A single numeric value between 0 and 1, inclusive.

Your final output must be a JSON object and must include no other text outside of the JSON.
'''
sbr_mrc = '''You are an expert superforecaster, familiar with the work of Philip Tetlock.

Question: {question}
Possible outcomes: Yes (1) or No (0)
Resolution criteria: {rules}
Scheduled close date: {expiration_time}
(Note: The question may resolve before this date.)

Instructions:
1. Identify multiple strong candidate reference classes that would be appropriate for generating base rates for this question.
2. For each of these reference classes, please provide a single best estimate of the base rate for the event within this reference class.
3. Compare and evaluate the different base rate estimates, and select the one you judge to be most appropriate and useful for this forecasting task.

Output your answer as a valid JSON object with exactly the following fields:
- "reasoning": A brief explanation of how the reference classes and the base rate estimates were derived and evaluated.
- "reference_classes": An array of strings, where each string is a clear and concise description of a reference class.
- "base_rates": An array of numeric values between 0 and 1, inclusive. Each base rate estimate should correspond to a reference class.
- "selected_base_rate": A single numeric value between 0 and 1, inclusive.

Your final output must be a JSON object and must include no other text outside of the JSON.
'''
mbr_mrc = '''You are an expert superforecaster, familiar with the work of Philip Tetlock.

Question: {question}
Possible outcomes: Yes (1) or No (0)
Resolution criteria: {rules}
Scheduled close date: {expiration_time}
(Note: The question may resolve before this date.)

Instructions:
1. Identify multiple strong candidate reference classes that would be appropriate for generating base rates for this question.
2. For each of these reference classes, please provide multiple strong candidate estimates of the base rate for the event within this reference class.

Output your answer as a valid JSON object with exactly the following fields:
- "reasoning": A brief explanation of how the reference classes and the base rate estimates were derived.

- "reference_classes": An array of strings, where each string is a clear and concise description of a reference class.
- "base_rates": A 2-dimensional array of numeric values between 0 and 1, inclusive. Each sub-array should correspond to a reference class and contain its base rate estimates.
'''
cbr_mrc = '''You are an expert superforecaster, familiar with the work of Philip Tetlock.

Question: {question}
Possible outcomes: Yes (1) or No (0)
Resolution criteria: {rules}
Scheduled close date: {expiration_time}
(Note: The question may resolve before this date.)

Instructions:
1. Identify multiple strong candidate reference classes that would be appropriate for generating base rates for this question.
2. For each of these reference classes, please provide multiple strong candidate estimates of the base rate for the event within this reference class.
3. Compare and evaluate the different base rate estimates, and select the one you judge to be most appropriate and useful for this forecasting task.

Output your answer as a valid JSON object with exactly the following fields:
- "reasoning": A brief explanation of how the reference classes and the base rate estimates were derived and evaluated.
- "reference_classes": An array of strings, where each string is a clear and concise description of a reference class.
- "base_rates": A 2-dimensional array of numeric values between 0 and 1, inclusive. Each sub-array should correspond to a reference class and contain its base rate estimates.
- "selected_base_rate": A single numeric value between 0 and 1, inclusive.

Your final output must be a JSON object and must include no other text outside of the JSON.
'''

# define function. takes a ticker symbol, returns a table with all the edsl reposnes. one col for each part of the full response, one col for base rate.

# define a fnuction that tkaes that table and returns the data nicely formatted as a table for printing.