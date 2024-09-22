API_KEY='' #KEY REMEMBER TO DELETE BEFORE PUSHING
MODEL_TYPE= 'gpt-4-turbo-preview' #MODEL TYPE
DOCS_DIR = "Docs/" #DIRECTORY OF PAPERS
SKIP = 2 #NUMBER OF PAGES TO READ AT A TIME
PROMPT = """
    json: GET THE MAIN IDEA!! You are to extract important entities, their definitions, overarching ideas,  and their relationships with one another from this paper. Don't copy the sentence word for word and split it up. Do not take all random relationships. Identify relationships that can help clinicians with diagnosis. . Will/May need to look across sections. Refrain from forming relationships unless text explicitly highlights or suggests that.
    
    Understand the sentence and determine the relationships between the subject and objects
    
    DO NOT use the word 'Depression' ALONE as a subject or object. Each block of text emphasizes different types of depression and you must include the type of depression the relationship is referring to.
    If the text is referring to all types of depression for that relationship, label it as "All Depression"
    The idea is that these relationships can be pieced together into a knowledge graph that a clinician can trace. Keep this in mind as you extract.
    
    Do not use any relationships other than these: 
    1. treatment:  IPT --> treatment for -> depression
    2. symptom: sadness -> symptom of -> depression
    3. example: medA --> example of -> antidepressant
    4. not effective: medA -> not effective for --> depression
    5. effective: medA -> effective for -> depression
    6. more effective: medA -> more effective than -> medB
    7. less effective: medA -> less effective than -> medB
    7. as effective as : medA -> as effective as -> medB
    8. side effects: sneezing --> side effect of -> medA
    9. treatment:  meditate --> treatment to -> reduce depression
    10. Same efficacy: medA -> Same efficacy as -> no meds
    11. Recommended first-line treatment: TreatA --> Recommended first-line treatment for --> illnesses
    12. High Efficiency: MedA -> High Efficiency for -> DiseaseA
    13. Less commonly used: MedB -> Less commonly used for -> Depression
    14. correlated: DiseaseA -> correlated with -> ProblemA
    15. More common than ... in ... : DiseaseA -> More common than -> DiseaseB -> in -> younger patients
    16. Concurrent comorbidity: Disease A -> Concurrent comorbidity -> IllnessC
    17. results: DiseaseA -> results -> faster treatment in young people
    18. predictor of: use of medA -> predictor of -> diseaseB
    19. Associateed with: Disease A -> associted with -> diases B
    20. definition: therapyA -> definition -> defA
    21: Correlation: ilnnessA -> correlation -> ilnessB
    22. Most common treatment: DiseaseA -> Most common treatment -> MedA
    23. Second most common treatment: DiseaseA - Second most common treatment -> MedA
    24. Use: MedA -> use -> decreasing symptomA or medA -> used on -> patients with problem B
    25. Properties: medC -> properties -> reduces this symptom by inihibiting that neuron
    26: form of: IllnessA -> form of -> CategroyA
    26. goal: MedA -> goal -> reduce anger
    27: requirements: treatmentA -> requirements -> patient under 23
    
    
    THESE SHOULD NOT BE THE SUBJ OR OBJ!!
    Each of these relationships is the base from which you can deviate a bit. Ex you can say treatment for, treatment with, treats, etc but stick 
    to the base idea of treating. Same applies for all relations    

    Examples: "bupropion is more likely than some ssris to lead to minimal weight gain or even weight loss."
        subj: bupropion 
        rel: side effects 
        obj: more likely than some ssris to lead to minimal weight gain or even weight loss minimal weight gain or even weight loss
    Examples: "venlafaxine's was seen to follow with less mental clarity than other medicines"
        subj: venlafaxine
        rel: side effect
        obj: less mental clarity



    Example:  As shown in Table 2, remission rates were significantly lower in patients with anxious depression,
    according to both the HAM-D criterion (22.2% versus 33.4%) and the QIDS-SR criterion (27.5% versus 38.9%). 
    Response rates were also significantly lower for patients with anxious depression (41.7% versus 52.8%). "
    
    Gives the rel(s): Anxious Depression -> finding -> low remission rates  and Anxious Depression -> finding -> low response rates 
    
    Present 1 dataframe in an easily readable and visually appealing format.
    The dataframe should explain the relationships between all subjects.
    It should have 4 headers, subj, rel, obj, reference. Reference should hold the exact sentence(s) (in quotes) that you used to get the relationship
    If you have object2 as a header, you must have a non-empty rel2 as a header. If thats not possible place the relationship in the next row
    
    
    Return a pandas dataframe structure called paper1
    Return a form of a dictionary of lists.
    Avoid entities and relationships that are more than a few words. If you need to list multiple drug names or treatments, list them in different rows
    
    
    """