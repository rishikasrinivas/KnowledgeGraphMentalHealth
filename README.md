
<div align="center">
  <img src="assets/header.svg" alt="Knowledge Graph For Mental Health" width="800"/>
</div>


<div align="center" style="font-family: Arial, Helvetica, sans-serif; color: #333; line-height: 1.6; padding: 20px;">
  <h3 style="font-weight: 600; font-size: 20px; max-width: 800px;">
    This repository contains tools and methodologies for evaluating Knowledge Graphs (KGs) generated by Large Language Models (LLMs) against manually annotated ground truth data. It also includes a user interface (UI) for managing KG data, as well as prompt engineering and evaluation techniques.
  </h3>
</div>


## 👥 Our Team 

<div align="center" style="border: 2px solid #aed4d2; padding: 10px; border-radius: 8px; max-width: 100%; overflow-x: auto;">
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/rishikasrinivas">
          <img src="https://github.com/rishikasrinivas.png?size=100" alt="Rishika" />
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/Kulieshova">
          <img src="https://github.com/Kulieshova.png?size=100" alt="Nataliia" />
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/anushkalimaye">
          <img src="https://github.com/anushkalimaye.png?size=100" alt="Anushka" />
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/Kymari28">
          <img src="https://github.com/Kymari28.png?size=100" alt="Kymari" />
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/Fernandadeltoro">
          <img src="https://github.com/Fernandadeltoro.png?size=100" alt="Fernanda" />
        </a>
      </td>
    </tr>
    <tr>
      <td align="center"><strong>Rishika Srinivas</strong> <br> @rishikasrinivas</td>
      <td align="center"><strong>Nataliia Kulieshova</strong> <br> @Kulieshova</td>
      <td align="center"><strong>Anushka Limaye</strong> <br> @anushkalimaye</td>
      <td align="center"><strong>Kymari Bratton</strong> <br> @Kymari28</td>
      <td align="center"><strong>Fernanda Del Toro</strong> <br> @Fernandadeltoro</td>
    </tr>
  </table>
</div>


## 🛠️ Technologies Used

### Core Technologies
- **Languages:** Python, HTML, CSS, JavaScript  
- **Database:** MongoDB  
- **AI Integration:** OpenAI API
- **User Interface:** React with Cytoscape.js for graph visualization


## 📝 Ground Truth Annotation  

Hand annotations were meticulously developed by team members, who manually reviewed every sentence across three provided PDFs. These annotations formed triplets structured as:  
- `subj` (Subject)  
- `rel` (Relationship)  
- `obj` (Object)  


## 💫 User Interface (UI)
  #### 1. Upload Files 📤
  <p align="center">
    <img src="assets/uploading.gif" alt="File Upload Demo" width="50%">
  </p>
  
  Easily import PDFs, which are converted into Knowledge Graphs (KGs) that extract clinical entities and relationships.
  
  #### 2. Fetch Previous Graphs 🔄
  <p align="center">
    <img src="assets/fetching.gif" alt="Fetch Previous Graphs Demo" width="50%">
  </p>
  
  Retrieve saved Knowledge Graphs for continued analysis or updates.
  
  #### 3. Search and Highlight 🔍
  <p align="center">
    <img src="assets/searching.gif" alt="Search Functionality Demo" width="50%">
  </p>
  
  A search-first design lets users quickly locate nodes or relationships. Results are highlighted in orange and zoomed in for clarity.
  
  #### 4. Dynamic Visualization 📊
  <p align="center">
    <img src="assets/visualization.gif" alt="Visualization Demo" width="50%">
  </p>
  
  Nodes represent clinical entities, and edges use color coding and varying thickness to show relationship categories and strength.
  The Relationship Table offers a legend with clickable colored circles for more details on each relationship.
  A magnitude table shows the significance of relationships.
  #### 5. Custom Filtering 🎯
  <p align="center">
    <img src="assets/filtering.gif" alt="Filtering Demo" width="50%">
  </p>
  
  Users can filter the graph to focus on specific relationship types (e.g., "Side Effects" or "Recommendations"), improving clarity without clutter.
  
  #### 6. Help Button ℹ️
  <p align="center">
    <img src="assets/help.gif" alt="Search Functionality Demo" width="50%">
  </p>
  
  An intuitive Help button offers guidance on the graph's features, ensuring accessibility for new users and clinicians unfamiliar with knowledge graphs.

### Design Highlights ✨

- **Brightside Health Branding**: The design aligns with **Brightside Health's brand** using calming blues, pastels, and creative accents like **color-coded edges** for a clean, engaging experience.
- **User-Centered Design**: Focuses on usability with:
  - **Interactive Relationship Table** for easy data interpretation
  - **Edge Thickness** to prioritize strong relationships for evidence-based decisions
  - **Search and Filtering** for focused, efficient navigation

## 📊 Evaluation Methods

### Evaluation Metrics Table 

| **Method**               | **Type**       | **Accuracy** | **Key Pitfalls**                   |
|---------------------------|----------------|--------------|-------------------------------------|
| Fuzzy Wuzzy              | Statistical    | 35.32%       | Low accuracy, only simple matches. |
| TF-IDF + Cosine Similarity | Statistical  | 36.28%       | Limited to vectorized text formats.|
| GPT Critic               | Model-Based    | 86.0%       | Utilizes an LLM to evaluate an LLM.|
| RAGA                     | Model-Based    | 69.67%      | Utilizes an LLM to evaluate an LLM.|
| G-Eval                   | Model-Based    | 46.60%        | Recommended use of medical domain dictionary.  |
| Precision                | Statistical  | 81.81%        | Can be mislead by cosine similarity|
| Hallucination            | Model-Based   |               | Utilizes an LLM to evaluate an LLM.|

### Detailed Evaluation Methodologies

#### 1. **Fuzzy Wuzzy**  
- **Evaluation Type:** Statistical  
- **Method:**  
   - Compare each row of the ground truth to each row of LLM output.  
   - Threshold for “matching” requires 70% or above similarity.  
- **Accuracy:** 35.32%  
- **Output:**  
   - Rows of LLM output that match the ground truth at or above 70% similarity.  
   - Only one triplet pair is found matching per threshold.  

---

#### 2. **TF-IDF Vector and Cosine Method**  
- **Evaluation Type:** Statistical, Feature-weighting  
- **Method:**  
   - Combine the triplet columns into a single string.  
   - Vectorize text using TF-IDF to convert it to numeric form.  
   - Compare each LLM row to each ground truth row using cosine similarity.  
- **Accuracy:** 36.28%  
- **Output:** Best matching ground truth row for each LLM output row.  

---

#### 3. **GPT Critic**  
- **Evaluation Type:** Model-Based  
- **Method:**  
   - Uses 10 worker threads to enable parallel comparisons.  
   - Compares each LLM output row with ground truth rows using GPT-3.5-turbo.  
   - Finds the best similarity score for each LLM output.  
- **Accuracy:** 86.0%  
- **Output:** Best ground truth match for each LLM output row.  

---

#### 4. **RAGA**  
- **Evaluation Type:** Model-Based  
- **Method:**  
   - Uses 10 worker threads to enable parallel comparisons.  
   - Compares each LLM output row with ground truth rows using GPT-3.5-turbo.  
   - Finds the best similarity score for each LLM output based on 3 criteria (Retrieval, Augmentation, and Generation).  
- **Accuracy:** 69.67%
    -  Retrieval: 61.0%
    -  Augmentation: 73.0%
    -  Generation: 75.0%
- **Output:** Best ground truth match for each LLM output row.  

---

#### 4. **G-Eval**  
- **Evaluation Type:** Model-Based  
- **Method:**
    - Define common synonyms and related terms in the medical domain
    - Calculate semantic similarity between two triples considering medical domain knowledge.
    - Evaluate matches between ground truth and LLM output
- **Accuracy:** 46.60%
- **Output:** Shows ground truth row with actual output row along with best evaluation score ranging from 0.10 to 0.80.

---

#### 7. **Precision** 
- **Evaluation Type:** Statistical: word match and cosine similarity 
- **Method:** Checking if the extracted relationship is in the source text or in the ground truth annotations  
- **Threshold for Matching:** 0.7
- **Precision Score:** 81.81%

---

#### 8. **Hallucination** 
- **Evaluation Type:** Statistical: Factual Alignment and Consistency
- **Method:** DeepEval Hallucination Metric
- **Threshold for Matching:** 0.5
- **Hallucination Score:** 


---

## Contribution  
We welcome contributions to improve the evaluation methods, refine the UI, or expand the dataset. Please feel free to submit issues or pull requests.  

---

## License  
This project is licensed under the [MIT License](LICENSE).  
