refine_template = ("""You are an expert at creating questions based on coding materials and documentation.
Your goal is to prepare a coder or programmer for their exam and coding tests.
we have recieved some practice questions to a certain extent: {existing_answer}.
we have the option to refine the existing questions or add new ones.
(only if necessary) with some more context below.

-----------
{text}
-----------

Given the new context, refine the original questions in English.
If the context is not helpful, please provide the original questions
QUESTIONS:
"""
)

prompt_template = """You are an expert at creating questions based on coding materials and documentation. 
Your goal is to prepare a coder or programmer for their exam and coding tests.
You do this by asking questions about the text below:
-------------
{text}
-------------

Create questions that will prepare the coders or programmmers for the exam and make sure not to lose any imporant information.

QUESTIONS:
"""