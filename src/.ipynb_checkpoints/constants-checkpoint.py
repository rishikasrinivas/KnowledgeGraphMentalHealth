API_KEY= '' #KEY REMEMBER TO DELETE BEFORE PUSHING
MODEL_TYPE= 'gpt-4-turbo-preview' #MODEL TYPE
DOCS_DIR = "Docs/" #DIRECTORY OF PAPERS
SKIP = 2 #NUMBER OF PAGES TO READ AT A TIME
TEMPERATURE=2
PROMPT =  """
     You are to extract important entities, their definitions, overarching ideas,  and their relationships with one another from this paper. Don't copy the sentence word for word and split it up. Do not take all random relationships. Identify relationships that can help clinicians with diagnosis. . Will/May need to look across sections. Refrain from forming relationships unless text explicitly highlights or suggests that.
    
    Understand the sentence and determine the relationships between the subject and objects
    
    DO NOT use the word 'Depression' ALONE as a subject or object. Each block of text emphasizes different types of depression and you must include the type of depression the relationship is referring to.
    If the text is referring to all types of depression for that relationship, label it as "All Depression"
    The idea is that these relationships can be pieced together into a knowledge graph that a clinician can trace. Keep this in mind as you extract.
    
    Do not use any relationships other than these (Note I've given the relationships and an example) :
        1. Associated with: 
        2. Results:
        3. Symptom: sadness -> symptom of -> depression
        4. Definition: axious depression -> definition -> major depressive disorder with high levels of anxiety symptoms 
        5. Correlation: 


        6. More common than … in …: Anxious depression --> more common than -> nonanxious depression -> in -> African American group, Hispanics, Primary Care Patients, Unemployed, Married then Divorced/Widowed, Less, Education, Public insurance, Lower-income


        7. Co-occuring with:
        8. Side effects:
        9. Goal:  TreatmentA -> goal -> Bs
        10. Treats: MedA --> treats -> B  OR TreatmentA --> treats -> B
        11. Entails: TreatmentA -> entails -> B,C,D,E
        12. Usage: A -> usage -> B
        14. Comparable to: A -> Comparable to -> B
        15. Properties: A -> properties -> B
        16. Form of: A -> Form of -> B
        17. Requirements: A -> requirements -> B
        18. Overview:  A -> overivew ->  B
        19. Benefit: A -> benefit -> B
        20. Treatment options: A -> Treatment options -> B
        21. Eligiblity: A -> eligibity -> B
        22. Consistency: A -> consistency -> B
        23. More effective: A -> more effective than -> medB OR treatA -> more effective for -> diseaseA
        24. Less effective: medA -> less effective than -> medB OR treatA -> less effective for -> diseaseA
        25. Same efficacy as ... for:  medA -> Same efficacy as -> medB OR treatA -> Same efficacy as -> treatB -> for -> diseaseA
        27. Specific efficacy in treating: medA -> Specific efficacy in treating -> atypical features, such as reactive moods, reverse neuro-vegetative symptoms, and sensitivity to rejection
        28. Highly effective: medA ->  Highly effective for -> diseaseB 
        29. Moderately effective: medA ->  Highly effective for -> diseaseB 
        30. More commonly used: medA ->  more commonly used -> diseaseB 
        31. Less commonly used: treatmentA ->  Less commonly used for -> diseaseB 
        32. Widely used: medA ->  widely used for -> diseaseB 
        33. example: medA --> example of -> antidepressant
        34. synonym: A -> synonym -> B
        35. not effective: medA -> not effective for -> diseaseB
    'synonym' should be frequently used to define concepts in the articles. Dont put subjects that are acronyms (IPT, ipt, etc) 
    make sure to use 'synonym' 

    
    
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

    Return the dataframe as a list of dictionaries in the structure of
    [
        dictionaries
    ]


    
    
    
    
    
    """
 