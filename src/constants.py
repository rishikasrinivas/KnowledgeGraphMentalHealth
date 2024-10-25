API_KEY= 
MODEL_TYPE= 'gpt-4-turbo-preview' #MODEL TYPE
DOCS_DIR = "Docs/" #DIRECTORY OF PAPERS
SKIP = 1 #NUMBER OF PAGES TO READ AT A TIME
TEMPERATURE=1
SAVE_FILE = 'DefinedRels_NoEX_4turbo.csv'
PROMPT =  """
     You are to extract important entities, their definitions, overarching ideas,  and their relationships with one another from this paper. Don't copy the sentence word for word and split it up. Do not take all random relationships. Identify relationships that can help clinicians with diagnosis. . Will/May need to look across sections. Refrain from forming relationships unless text explicitly highlights or suggests that.
    
    Understand the sentence and determine the relationships between the subject and objects
    
    DO NOT use the word 'Depression' ALONE as a subject or object. Each block of text emphasizes different types of depression and you must include the type of depression the relationship is referring to.
    If the text is referring to all types of depression for that relationship, label it as "All Depression"
    The idea is that these relationships can be pieced together into a knowledge graph that a clinician can trace. Keep this in mind as you extract.
    
    Do not use any relationships other than these (Note I've given the relationships and explained when to use it) :
        1. Associated with: use this to explain when a disease has some effect on someones life. Don't use it to define a disease. For example dont say 'depression -> associated with -> 
        2. Results: use this when the sentence shows events, observations and/or results.
        3. Symptom: when the subject/object is a sign of the object/subject
        4. Definition: when the text explains the meaning of a disease or word
        5. first-line treatment: when the reference string (ref) mentions that something was used as a first-line treatment.NOTE DO NOT USE UNLESS THE TEXT YOU'RE REFERENCING SPECIFICALLY MENTIONS THE WORDS 'FIRST-LINE TREATMENT'. NOTE: 'MOST FREQUENT' AND OTHER SYNONYMS DO NOT COUNT AS 'FIRST-LINE TREATMENT'
        6. More common than … in …: Anxious depression --> more common than -> nonanxious depression -> in -> African American group, Hispanics, Primary Care Patients, Unemployed, Married then Divorced/Widowed, Less, Education, Public insurance, Lower-income


        8. Side effects: When the text demonstrates effects on the patient as VERBS, samples: nausea, vomiting, etc. This is different from results
        9. Goal:  When the text explains the expected outcone or purpose of using treatment or medication
        10. Treats: When the text states that a medicine or treatment 'treats' or some synonym of that
        11. second-line treatment:  when the reference string (ref) mentions that something was used as a second-line treatment. NOTE DO NOT USE UNLESS THE TEXT YOU'RE REFERENCING SPECIFICALLY MENTIONS THE WORDS 'SECOND-LINE TREATMENT'. NOTE: 'SECOND MOST FREQUENT' AND OTHER SYNONYMS DO NOT COUNT AS 'SECOND-LINE TREATMENT'
        14. Comparable to: A -> Comparable to -> B
        15. Properties: When the text defines the qualities of a medicine. 
        16. Form of: When the text an idea that is similar to another idea, but is different
        17. Requirements: When the text mentions the prerequesities or required attributes of a patient in order to use a plan
        18. Overview: When the text gives a description of HOW a treatment is used ex and will often use ACTION Verbs: Combines elements of CBT with mindfulness-based stress reduction. The subject should be a treatment plan like a therapy. Not a drug nor a disease
        19. Benefits: When the text mentions what group benefits from the medicine/treatment OR if it mentions something positive abput a treatment or medicine
        20. Treatment options: When the text mentions different ideas for treatments for a disease or different treatment ideas within an overarching treatment idea 
        21. Eligiblity: When the text mentions prerequisites or preferences for the target patients
        22. Consistency: When the text mentions whether something yielded consistent results or not
        23. More effective: when the text mentions if something was more effective than somethign else
        24. Less effective: when the text mentions if something was less effective than somethign else
        25. Same efficacy as ... for:  when the text mentions if something has the same efficieny  than somethign else
        27. Specific efficacy in treating: when the text mentions if something was a specific efficacy for   somethign  
        28. Highly effective: when the text mentions if something was highly effective
        29. Moderately effective: when the text mentions if something was moderately effective
        30. More commonly used: when the text mentions if something was more commonly used
        31. Less commonly used:  when the text mentions if something was less commonly used
        32. Widely used: medA ->   when the text mentions if something was widelt used
        33. example: when the text gives a subtopic from an overaching topic. Like a medicine that they say is an antidepressant. Or a disease they say is an example of something. Or a treatment that has different forms or branches
        34. short form: When the text says something is a short form of something else or something in the format of (word (short-form), ex: challenge advisor (CA))
        35. not effective: when the text says something was not effective for some disease or some synonym of not effective 
        36. dosage: when the text provides specific numbers claiming them to be dosages provided 
        37. details: when the text proides speicifc information regarding treatments including duration, process, etc This is different from dosage in that it doesnt apply to information in the text to pertain to amount of tablets or drugs given. 
    'synonym' should be frequently used to define concepts in the articles. Dont put subjects that are acronyms (IPT, ipt, etc) 
    make sure to use 'synonym' 

    Follow the instructions for when to use each relation please!
    
    THESE SHOULD NOT BE THE SUBJ OR OBJ!!
    Each of these relationships is the base from which you can deviate a bit. Ex you can say treatment for, treatment with, treats, etc but stick 
    to the base idea of treating. Same applies for all relations    

    Examples: "bupropion is more likely than some ssris to lead to minimal weight gain or even weight loss."
        subj: bupropion 
        rel:  side effects 
        obj:  more likely than some ssris to lead to minimal weight gain or even weight loss minimal weight gain or even weight loss
    Examples: "venlafaxine's was seen to follow with less mental clarity than other medicines"
        subj: venlafaxine
        rel:  side effect
        obj:  less mental clarity



    Example:  As shown in Table 2, remission rates were significantly lower in patients with anxious depression,
    according to both the HAM-D criterion (22.2% versus 33.4%) and the QIDS-SR criterion (27.5% versus 38.9%). 
    Response rates were also significantly lower for patients with anxious depression (41.7% versus 52.8%). "

    Gives the rel(s): Anxious Depression ->  side effects -> low remission rates  and Anxious Depression -> side effects -> low response rates 

    Develop relationships that all connect to depression. Meaning as subj, have A FORM OF DEPRESSION (following the 'depression' rules mentioned) as the subject, then a relation that connects depression to the object

    
    Develop a dataframe that should have 4 headers, subj, rel, obj, ref. Reference should hold the exact sentence(s) (in closed quotes) that you used to get the relationship, This dataframe should explain the relationships between all subjects.

    Return the dataframe as a list of dictionaries in the structure of [, <enter>, dictionaries, <enter>, ]
    [
        dictionaries
    ]


    
    
    
    
    
    """
 