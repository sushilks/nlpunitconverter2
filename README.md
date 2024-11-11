# nlpunitconverter v2
A natural language unit conversion tool (Based on LLM)

I had tried to create a natural language input for a cli back in 2013 [nlpunitconverter v1](https://github.com/sushilks/nlpUnitConverter) and had very limited success. 
Since then with the LLM's this problem has been solved and this project captures how to create a tool based flow with the help of llms for solving a simple problem of unit conversion and simple math. 

The tool uses [langchain](https://github.com/langchain-ai/langchain) / [langgraph](https://github.com/langchain-ai/langgraph) for processing the llm output and executing the tools. 

for unit conversion the tool uses [pint](https://github.com/hgrecco/pint)
The entier pint [unit definition file](https://github.com/hgrecco/pint/blob/master/pint/default_en.txt) is fead verbatim into the llm as a prompt before the query is posed to the llm.

# to setup 
install all the packages by running 
```
make dep

or 

pip install -r ./requirements.txt
```

# to check run options 
help 
```
# base help 
python -m nlc --help
# example help with process command 
python -m nlc process --help
```

# to run queries from command line 
Default provider is OpenAI and default models is gpt-4o


```
bash> python -m nlc process -t "How many Kilos are there in 30lb?"

Response >  There are approximately 13.61 kilograms in 30 pounds.
```
# running with tool log enabled 
Enableing tool log will show all the calls made to the tool 
```
bash> python -m nlc process -t "How many Kilos are there in 30lb?"  -l
	step[0] ::: unit_convert is called with arguments {'a_number': 30, 'a_unit': 'pound', 'b_unit': 'kilogram'} and got result 13.607771100000003

Response >  There are approximately 13.61 kilograms in 30 pounds.
```

A more complicated query that uses some math tools 
```
bash> python -m nlc process -t "what is the weight of each part in kg when I divide a 12lb sack into 4 parts?" -l
	step[0] ::: unit_convert is called with arguments {'a_number': 12, 'a_unit': 'pound', 'b_unit': 'kilogram'} and got result 5.443108440000001
	step[1] ::: division is called with arguments {'x': 5.443108440000001, 'y': 4} and got result 1.3607771100000003

Response >  When you divide a 12-pound sack into 4 equal parts, each part weighs approximately 1.36 kg.
```


A math example that calls tools for each task
```
bash> python -m nlc process -t "what is 3 multiplied by 9 added to 45 then divide all by 6?"  -l
	step[0] ::: multiplication is called with arguments {'x': 3, 'y': 9} and got result 27
	step[1] ::: addition is called with arguments {'x': 27, 'y': 45} and got result 72
	step[2] ::: division is called with arguments {'x': 72, 'y': 6} and got result 12.0

Response >  To solve the expression step-by-step:

1. Multiply 3 by 9:
   \(3 \times 9 = 27\)

2. Add the result to 45:
   \(27 + 45 = 72\)

3. Divide the total by 6:
   \(72 \div 6 = 12\)

So, the final result is 12.0.
```

another math example
```
bash> python -m nlc process -t "What is the sum of 1 2 9 and 10?" -l
	step[0] ::: addition is called with arguments {'x': 1, 'y': 2} and got result 3
	step[1] ::: addition is called with arguments {'x': 3, 'y': 9} and got result 12
	step[2] ::: addition is called with arguments {'x': 12, 'y': 10} and got result 22

Response >  The sum of the numbers 1, 2, 9, and 10 is 22.
```



# To process a file with multiple line 
```
bash> python -m nlc file -f ./sample_query.txt
```