API_KEY= ''
MODEL_TYPE= 'gpt-4-turbo-preview' #MODEL TYPE
DOCS_DIR = "Docs/" #DIRECTORY OF PAPERS
SKIP = 3 #NUMBER OF PAGES TO READ AT A TIME
TEMPERATURE=1

MONGO_URI="mongodb://127.0.0.1:27017/"
SAVE_FILE = '/Users/rishikasrinivas/KnowledgeGraphMentalHealth/NewRels_Skip4.csv'
PROMPT =  """
     You are to extract important entities, their definitions, overarching ideas, and their relationships with one another from this paper. Do not take all random relationships. Identify relationships that can help clinicians with diagnosis. Will need to look across sections. Refrain from forming relationships unless the text explicitly highlights or suggests that.
    
    Understand the sentence and determine the relationships between the subject and objects
    
    DO NOT use the word 'Depression' ALONE as a subject or object. Each block of text emphasizes different types of depression and you must include the type of depression the relationship is referring to. In some places treatments, illnesses, and side effects may be given as a shortened form but in this case, still present it in its complete form.

    If the text is referring to all types of depression for that relationship, label it as "All Depression"
    The idea is that these relationships can be pieced together into a knowledge graph that a clinician can trace. Keep this in mind as you extract.

    If a sentence uses one of these relationship words, use that specific relationship word for that triplet (subj, rel, obj)
    Do not use any relationships other than these (Note I've given the relationships and explained when to use it) :
    
        1. Subset: Use this ONLY for types of another topic. This means that if there is an illness or treatment or side effect that belongs to a broader category, explain the relationship like x -> subset -> boarderCategory.
            For example: DepressionTypeA -> subset -> Depression, TreatmentA1 -> subset -> TreamentA

            
        2. Associated with: use this to explain when a disease has some effect on someones life. Don't use it to define a disease. For example do not say 'depression -> associated with -> disease/treatment 
        
        3. Results: use this when the sentence shows events, observations and/or results. This rel will be used when there is a general description of the outcomes of a test/experiment and when there is a sense of comparison in the sentences of the text. This is different from side effects. You will not use this relationship if the description following an experiment indicates an effect of the experiment on a patients health.
        
        4. Symptom: when the subject indicates the potential presence of the object
    
        5. Definition: when the text explains the meaning of a word. This word can be an illness, treatment, side effect, or medicine
        
        6. first-line treatment: when the reference string (ref) mentions that something was used as a first-line treatment.NOTE DO NOT USE UNLESS THE TEXT YOU'RE REFERENCING SPECIFICALLY MENTIONS THE WORDS 'FIRST-LINE TREATMENT'. NOTE: 'MOST FREQUENT' AND OTHER SYNONYMS DO NOT COUNT AS 'FIRST-LINE TREATMENT'
        
        7. More common than … in …: Anxious depression --> more common than -> nonanxious depression -> in -> African American group, Hispanics, Primary Care Patients, Unemployed, Married then Divorced/Widowed, Less, Education, Public insurance, Lower-income

        8. Side effects: When the text demonstrates effects on the patient as VERBS, samples: nausea, vomiting, etc. This is different from results. 
        
        9. Goal:  When the text explains the expected outcone or purpose of using treatment or medication
        
        10. Treats: When the text states that a medicine or treatment 'treats' or some synonym of that
        
        11. second-line treatment:  when the reference string (ref) mentions that something was used as a second-line treatment. NOTE DO NOT USE UNLESS THE TEXT YOU'RE REFERENCING SPECIFICALLY MENTIONS THE WORDS 'SECOND-LINE TREATMENT'. NOTE: 'SECOND MOST FREQUENT' AND OTHER SYNONYMS DO NOT COUNT AS 'SECOND-LINE TREATMENT'
        
        14. Comparable to: When the text specifically mentions that two treatments , two medicines, or 2 illnesses are comparable 
        
        15. Properties: When the text defines the qualities of a medicine. 
        
        16. Form of: When the text an idea that is similar to another idea, but is different
        
        17. Requirements: When the text mentions the prerequesities or required attributes of a patient in order to use a plan
        
        18. Overview: When the text gives a description of HOW a treatment is used ex and will often use ACTION Verbs: Combines elements of CBT with mindfulness-based stress reduction. The subject should be a treatment plan like a therapy. Not a drug nor a disease
        
        19. Benefits: When the text mentions what group benefits from the medicine/treatment OR if it mentions something positive abput a treatment or medicine
        
        20. Treatment options: When the text mentions different ideas for treatments for a disease or different treatment ideas within an overarching treatment idea 
        
        21. Eligiblity: When the text mentions prerequisites or preferences for the target patients
        
        22. Consistency: When the text mentions whether medicine/treatment yielded consistent results or not
        
        23. More effective: when the text mentions if medicine/treatment was more effective than another medicine/treatment
        
        24. Less effective: when the text mentions if one medicine/treatment was less effective than another medicine/treatment
        
        25. Same efficacy as ... for:  when the text mentions if something has the same efficieny  than somethign else
        
        27. Specific efficacy in treating: when the text mentions if something was a specific efficacy for treating an illness  
        
        28. Highly effective: when the text mentions if  medicine/treatment was highly effective
        
        29. Moderately effective: when the text mentions if  medicine/treatment was moderately effective
        
        30. More commonly used: when the text mentions if  medicine/treatment was more commonly used
        
        31. Less commonly used:  when the text mentions if  medicine/treatment was less commonly used
        
        32. Widely used: when the text mentions if  medicine/treatment was widely used
        
        33. example: when the text gives a subtopic from an overaching topic. Like a medicine that they say is an antidepressant. Or a disease they say is an example of something. Or a treatment that has different forms or branches
        
        34. short form: When the text says something is a short form of something else or something in the format of (word (short-form), ex: challenge advisor (CA))
        
        35. not effective: when the text says something was not effective for some disease or some synonym of not effective 
        
        36. dosage: when the text provides specific numbers claiming them to be dosages provided 
        
        37. details: when the text proides speicifc information regarding treatments including duration, process, etc This is different from dosage in that it doesnt apply to information in the text to pertain to amount of tablets or drugs given. 
    'synonym' should be frequently used to define concepts in the articles. Dont put subjects that are acronyms (IPT, ipt, etc) 
    make sure to use 'synonym' 

    THESE SHOULD NOT BE THE SUBJ OR OBJ!!

    Follow the instructions for when to use each relation please! And try to use each relation 1 time but if a relation doesn't apply to the text, DO NOT use it
    
    
    Develop a dataframe that should have 6  headers, subjSummary, subj, rel, obj, objSummary ref. Reference should hold the exact sentence(s) (in closed quotes) that you used to get the relationship, This dataframe should explain the relationships between all subjects and for each subject and object. Be consistent. So if at one point you use an abbreviation for the subjSummary or objSummary, utilize that abbreviation across all summries where you would use either that abbreviation or the whole form.

    
    If the subject and/or object are more than 3 words, leaf it as is in the subj column but also summarize it into 1 word and store that as subjSummary or objSummary respectively. If the subject and/or object are less than 3 words just copy the subject/object into the subjSummary/objSumary segment. 


    Go through all the relationships and make sure there are no inconsistencies and no repeats and everything is factual

    Return the data frame as a list of dictionaries in the structure of [, <enter>, dictionaries, <enter>, ]
    [
        dictionaries
    ]

    
    
    
    """

'''
 medicine/treatment
'''
 