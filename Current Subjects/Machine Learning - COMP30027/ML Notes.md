COMP300027 - Machine Learning, The University of Melbourne
=========

LSM Notes: https://www.overleaf.com/1157211432bhswsxwjccmk 

## Lecture 2: Basics of Machine Learning
#### Some Terminology
- Instances (exemplars) are the rows of a dataset
- Attributes (features) are the columns of a dataset
- Concepts (labels or classes) are things we aim to learn from the dataset
- Nominal Quantities (categorical or discrete) have no relation between labels (`sunny, hot, rainy`)
- Ordinal Quantities have an implied ordering on the values (`cold < mild < hot`)
- Continuous Quantities are real-valued attributes with a defined zero point and no explicit upper bound

#### Methods
- **Supervised** methods have prior knowledge to a closed set of classes. Essentially "feed it" data and hope it can train itself to predict it.
- **Unsupervised** methods will dynamically discover "classes". These don't require labels and will train itself to categorize instances (usually mathematically).

#### Classification
- The learning algorithm is provided with a set of classified **training data**
- Uses the Split -> Test -> Train method to test for accuracy
- A **supervised** algorithm
- Works with *discrete* or *categorical* data

#### Clustering
- Finds groups of items that are similar 
- Works purely on a distance metric and therefore *does not* require a label
- Performance is subjective and is problematic when evaluating
- An **unsupervised** algorithm

#### Regression
- Technically a type of *Classification Learning*, but works with continuous data
- A **supervised** algorithm

#### Association Learning
- Detects patterns, associations or correlations among a set of items or objects
- Any kind of association is considered interesting with no "care" for what we want to predict
- An **unsupervised** algorithm

#### Values
- **Missing Values** can be caused by:
    - Malfunction equipment
    - Changes in experimental design
    - Collation of different datasets
    - A non-possible measurement
- **Inaccurate Values** can be caused by:
    - Errors or omissions that don't impact the data (`Age of Customer, Location`)
    - Typos when entering data
    - Deliberately false data to protect their own privacy

## Lecture 3: Revision of Probability Theory
#### Bayes Rule
$Pr(A|B) = \frac{Pr(A\cap B)}{Pr(B)} = \frac{Pr(B|A)Pr(A)}{Pr(B)}$
- $Pr(A)$, the prior, is the initial degree of belief in $A$
- $Pr(A|B)$, the posterior, is the degree of belief having counted for B

#### Some distributions you should know
- Bernoulli
- Binomial
- Multinomial

#### Entropy (Information Theory)
**Entropy**: a measure of *unpredictability* on the information required to predict an event.  
The entropy (in *bits*) of a discrete r.v $X$ is defined as:  

$H(X) = -\sum^n_{i=1}Pr(x_i)\log_2(Pr(x_i))$ where $H(X) \in [0, \log_2(n)]$.
- A **high** entropy value means $X$ is unpredictable. Each outcome gives *one bit* of information
- A **low** entropy value means $X$ is more predictable. We don't learn anything once we see the outcome

#### Entropy Example:
Let $Pr(X = Heads) = 0.9, Pr(X = Tails) = 0.1$. Then  

$
H(X) = -[Pr(X = Heads)\log_2(Pr(X = Heads)) + Pr(X = Tails)\log_2(Pr(X = Tails))] \\
= -[0.9\log_2(0.9) + 0.1\log_2(0.1)]\\
= 0.47
$

#### Estimating Probabilities (Frequentist Method)
If we don't have the whole population, we can take a sample of it to estimate the relative distribution (MLE in stats). 

$\hat{Pr}(X=x) = \frac{freq(x)}{\sum^k_{i=1}freq(x_k)} = \frac{freq(X)}{N}$

$\hat{Pr}(X=x,Y=y) = \frac{freq(x,y)}{N}$

$\hat{Pr}(X=x|Y=y) = \frac{freq(x,y)}{N}$

## Lecture 4: Naive Bayes
#### The Naive Bayes Implementation
The Naive Bayes assumes that all probabilities are independent. 

We have that for ever class $j$,

$Pr(x_1,x_2,\dots,x_n | c_j) \approx \prod_{i=1}P(x_i | c_j)$

This is called a **conditional independence assumption**, and makes Naive Bayes a tractable method. 

```python
for every test instance:
    for every attribute in test instance:
        for every class label:
            calculate the probability (conditional independence)
    return the largest probability and find the corresponding class label
```

#### Probabilistic Smoothing
If you note the formula before, then multiplying any probability of 0 results in 0. This means that unseen events become an "impossible" event, which is untrue.

**Using epsilon:**  
To combat this, we assume that **no event is impossible** (i.e. every probability is greater than 0). This is implemented by replacing 0 with a value $\epsilon\rightarrow 0$, where $1+\epsilon \approx 1$, so we don't need change our approach with non-zero probabilities. 

**Using Laplace smoothing (or add-one):**   
BETTER ALTERNATIVE - *add-k smoothing*.  
Laplace smoothing essentially gives unseen events a count of 1. Then, all counts are increased to ensure that monotonicity is maintained. Let $V = \textrm{Number of attributes},

Then for every class $j$, and event $i$,  
$\hat{Pr}(x_i | c_j) = \frac{1 + freq(x_i, c_j)}{V + freq(c_j)}$

#### Missing Values

- If a value is missing in a test instance, it is possible to just simply ignore that feature for the purposes of classification.  
- If a value is missing in a training instance, then it is possible to simply have it no contribute to the attribute-value counts/probability estimates for that feature. 

```python
if value == missing:
    pass
```

## Lecture 5: Evaluation Part 1
The basic evaluation metric is *Accuracy*.  

$\textrm{Accuracy} = \frac{\textrm{Number of correctly labelled test instances}}{\textrm{Total number of test instances}}$  

Quantifies how frequently the classifier is correct, with respect to a fixed dataset with known labels. 

#### Strategies

Two main different strategies to evaluate your model.  


**Holdout:**  
- Each instance is randomly assigned as either a training instance or a test instance.
- The dataset is effectively partitioned with no overlap between datasets
- You build the model based on the trainin instance, and evaluate the trained model with the test instances
- Common train - test splits are: 50 - 50, 80 - 20, 90 - 10
- Advantages:
  - Simple to work with and implement
  - Fairly high reproducibility
- Disadvantages:
  - The split ratio affects the estimate of the classifier's behavior
    - Lots of test instances with few training instances leaves the model to build an inaccurate model
    - Lots of training instances with few test instannces leaves the model to be accurate, but the test data may not be representative

**Repeated Random Subsampling:**  
- Works similar to **holdout**, but over several iterations
  - New training set and test set are randomly chosen each iteration
  - The size of train-test split is fixed accross the iterations
  - A new model is built every iteration
- Advantages: 
  - Average holdout method tends to produce more reliable results
- Disadvantages:
  - Slower than the holdout method (by a constant factor)
  - A wrong choice of train-test split can lead to highly misleading results

**Cross-Validation:**  
- The **usual preferred method of evaluation**
- The dataset is progressively split into a number of $m$ partitions
  - One partition is used as test data
  - The other $m - 1$ partitions are used as training data
  - Evaluation metric is aggregated across the $m$ partitions
    - Take the average
    - Sum the accuracy across iterations
- Why is this better than holdout / repeated random subsampling?
  - Every instance is a test instance (for some partition)
    - Similar to testing on the training data, but without the dataset overlap
  - Takes roughly the **same time** as Repeated Random Subsampling
  - Can be shown to **minmise the bias and variance** of our estimates of the classifier's performance
- How big is $m$?
  - Small $m$: more instances per partition, **more variance** in performance estimates
  - Large $m$: fewer instances per partition, **less variance** but slower
  - We usually choose $m = 10$ which mimics the 90 - 10 holdout strategy
- An alternative is to use $m = N,\textrm{ the number of test instances}$ - called the **Leave One Out Cross Validation**
  - Maximises the training data for the model
  - Mimics the actual testing behaviour
  - **Far too slow to use in practice**

**Stratification:**  
- A type of inductive learning hypothesis
  - Any hypothesis found to approximate the target function over a large training dataset will also approximate the target function well over any **unseen** test examples
- However, machine learning suffers from **inductive bias** meaning assumptions must be made about the data to build a model and make predictions
- Stratification assumes that the **class distribution** of unseen instances will share the same distribution of see ninstances
  - Class distribution is used here to extend definitions from continuous domain to discrete domain 

#### Determining if a Classifier is Good
- True Positive (TP) are instances where we predicted label `A` and the actual label was `A`
- False Positive (FP) are instances where we predicted label `A` but the actual label was `B`
- True Negative (TN) are instances where we predicted label `?` and the actual class label was `?`
- False Negative (FN) are instances where we predicted label `A` but the actual class label was `?`


We want **TRUE** negatives and positives (correctly predicted).

A classifier may then classify:
- An Interesting Instance as I if it is True Positive (TP)
- An Interesting Instance as U if it is False Negative (FN)
- An Uninteresting Instance as I if it is False Positive (FP)
- An Uninteresting Instance as U if it is True Negative (TN)

#### Classification Accuracy
Classification Accuracy is the proportion of instances for which we have correctly predicted the label, given as  

$\textrm{Classification Accuracy} = \frac{TP + TN}{TP + FP + FN + TN}$

#### Error Rate
An Error Rate can also be used, where $ER = 1 - \textrm{Classification Accuracy}$

#### Precision and Recall
- Precision: How often are we correct when we predict 
- (Cancer Patients: how many we predicted to have cancer correctly / how many we predicted to have cancer overall)

  
    $\textrm{Precision} = \frac{TP}{TP + FP}$

- Recall: What proportion of the predictions have we correctly predicted 
- (Cancer Patients: how many we predicted to have cancer correctly / actual number of patients with cancer)

  - $\textrm{Recall} = \frac{TP}{TP + FN}$


High precision gives low recall, and high recall gives low precision. But, we want both precision and recall to be high. A popular metric that evaluates this is called the **F-Score**.

$F_\beta = \frac{(1+\beta^2)2PR}{\beta^2P + R}$  

$F_1 = \frac{2PR}{P + R}$

#### Baseline vs Benchmark
A **Baseline** is a naive method which we would expect any reasonably well-developed method to better it.
- Important in establishing whether any proposed method is doing better than "dumb and simple"
- Valuable in getting a sense for the intrinsic difficulty of a given task
  - Baseline accuracy of 5% vs 99%

A **Benchmark** is an established rival technique which we are pitching our method against (does our model perform better)

#### Types of Baseline
**Random Baseline:**  
- Method 1: randomly assign a class to each test instance
- Method 2: randomly assign a class $c_k$ to each test instance, weight the class assignment according to $Pr(c_k)$
  - Assumes we know the class prior probabilities

**Zero-R (or Majority Class):**  
- Method: classifies all instances according to the most common class in the training data
- Not appropriate if the majority class is "FALSE" and the learning task is to identify the "TRUE"s

**One-R:**
Creates a single rule for each attribute in the training data, then selects the rule with the **smallest error rate** as its "one rule"
- Method: create a *decision stump* for each attribute with branches for each value, then populate the leaf with the majority class at that leaf. Then, select the decision stump which leads to the lowest error rate over the training data  
- Out of the training instances, how many `attribute value` correspond to `label`. Then, pick the `attribute` with the smallest error rate.  

```
for each attribute:
    for each value of the attribute:
        count class frequency corresponding to value.
        find most frequent class corresponding to value.
        set correct = most frequent class label corresponding to value.
        error rate is number of "other" classes.
    calculate total error rate of the attribute
choose the attribute whose with the smallest error rate
```

- Advantages:
  - Simple to understand and implement
  - Suprisingly good results
- Disadvantages:
  - Unable to capture attribute interactions
  - Bias towards attributes with several possible values

## Lecture 6: Decision Trees (ID3)
- Basic method: construct decision trees in recursive divide-and-conquer fashion
- We want the smallest tree (minimizes the errors)
```python
def ID3(root):
    if all instances at root have same class:
        return 
    else:
        - select a new attribute to use in a partitioning root node instance
        - create a branch for each attribute value and partition up root node instances according to each value
        for each leaf node:
            ID3(leaf)
```

#### Information Gain
The expected *reduction* in entropy caused by knowing the value of an attribute.  
Compare:
- The entropy before splitting the tree using the attribute's values
- The weighted average of the entropy over the children after the split (known as **Mean Information**)  

If the entropy *decreases*, then we have a better tree (more predictable)

#### Mean Information
We calculate the mean information for a tree stump with $m$ attribute values as:  

$\textrm{Mean Info}(x_1,x_2,\dots,x_m) = \sum^m_{i = 1}Pr(x_i)H(x_i)$

where $H(x_i)$ is the entropy of the class distribution for the instances at node $x_i$.

#### Analysis of Information Gain
Information gain tends to prefer highly-branching attributes
- A subset of instances is more likely to be homogeneous (all of a single class) if there are only a few instances
- Attributes with many values will have fewer instances at each child node

These factors may result in overfitting or fragmentation

#### Gain Ratio
- Gain Ratio (GR) reduces the bias for information gain towards highly branching attributes by normalizing relative to the split information
- Split Info (SI) (or called Intrinsic Value) is the entropy of a given split (evenness of the distribution of instances to attribute values)

$GR(R_A | R) = \frac{H(R) - \sum^m_{i=1}Pr(x_i)H(x_i)}{-\sum^m_{i=1}Pr(x_i)log_2(Pr(x_i))}$

#### Stopping Criteria
ID3 is defined in a way such that:
- The Info Gain / Gain Ratio allows us to choose the seemingly better attribute at a given node
- It is an approximate indication of how much absolute improvement we expect from partitioning the data according the values of a given attribute
- An Info Gain of $0$, or close to $0$ means that there is no improvement and is often unjustifiable
- A typical modification of ID3 is to choose the best attribute given it is greater than some threshold $\tau$
- Can be pruned to drop undesirable branches with close to no Info Gain / Gain Ratio improvements 

#### ID3 Decision Tree Analysis
- Highly regarded among basic supervised learners
- Fast train and classification
- Susceptible to the effects of irrelevant features
- Alternative Decision Trees:
  - **Oblivious Decision Trees** require the same attribute at every node in a layer
  - **Random Trees** only use samples of the possible attributes at any given node
    - Helps to account for irrelevant attributes
    - Basis for a better Decision Tree variant called the **Random Forest**

## Lecture 7: Instance Based Learning (IBL)
#### Similarity
**Jaccard Similarity:**  

$sim_J(A, B) = \frac{|A\cap B|}{|A\cup B|}$

**Dice Coefficient:**  

$sim_D(A , B) = \frac{2|A\cap B|}{|A| + |B|}$

#### Feature Vectors
- A feature vector is an n-dimensional vector of features that represent some object
- A feature or attribute is any distinct aspect, quality, or characteristic of that object

A vector locates an instance as a point in an orthogonal n-space. The angle of the vector in that n-space is determined by the relative weight of each term (m-attributes).
- Similarity:
    - A numerical measure of how similar two vectors are
    - Higher measure for closer similarity
    - Often falls between [0, 1]
- Dissimilarity:
    - A numerical measure of how different two vectors are
    - Lower measure for **closer** similarity (higher measure for **more** difference)
    - Minimum (or close to no) dissimilarity is often 0, with a varying upper limit

#### Distance Metrics
**Hamming Distance:**
$d_H(A,B) = \sum^n_{i=1}[0\textrm{ if }a_i == b_i\textrm{ else }1]$

**Euclidean Distance:**  
- Given two items $A$ and $B$, and their feature vectors $\mathbf{a}$ and $\mathbf{b}$, we can calculate their distance $d$ in Euclidean space:

$d(A, B) = \sqrt{\sum^n_{i=1}(a_i - b_i)^2}$

**Manhattan Distance:**  
- Also know as $L_1$ distance (same as AI)
- Given two items $A$ and $B$, and their feature vectors $\mathbf{a}$ and $\mathbf{b}$, we can calculate their similarity via their distance $d$ based on the absolute differences of their cartesian coordinates:

$d(A, B) = \sum^n_{i=1}|a_i - b_i|$

**Cosine Similarity:**  
- Given two items $P$ and $Q$, and their feature vectors $\mathbf{p}$ and $\mathbf{q}$, we can calculate their similarity via their **vector cosine**:

$cos(P,Q) = \frac{\mathbf{p}\cdot \mathbf{q}}{|\mathbf{p}||\mathbf{q}|} = \frac{\sum^n_{i=1}p_iq_i}{\sqrt{\sum^n_{i=1}p^2_i}\sqrt{\sum^n_{i=1}q^2_i}}$

#### Nearest Neighbour
The nearest neighbour is defined as the closest object from your object, using a specified distance metric.

In classification, we give class assignments of existing data points, and classify them according to $k$ nearest neighbours.

**1-NN:**
- Classify the test input according to the class of the *closest* training instance

**$K$-NN:** 
- Classify the test input according to the *majority* class (or mode class) of the $K$ nearest training instances

**Weighted $K$-NN:**
- Classify the test input according to the weighted accumulative class of the $K$ nearest training instances, where weights are based on similarity of the input to each of the $K$ neighbours

**Offset-Weighted $K$_NN:**
- Classify the test input according to the weighted accumulative class of the $K$ nearest training instances, where weights are based on similarity of the input to each of the $K$ neighbours, factoring in an offset for the prior expectation of a test input being a member of that class

#### Weight Strategies (Majority Class, ILD, and ID)
These are the notable strategies for weighing:
- Give each neighbour equal weight (classify according to the **majority class** of set of neighbours)
- Weight the vote of each instance by its **inverse linear distance (ILD)** from the test instance:
    $w_j = \frac{d_k - d_j}{d_k - d_1}$ if $d_j \neq d_1$ else $w_j = 1$, where $d_1$ is the nearest neighbour, and $d_k$ is the furthest neighbour
- Weight the vote of each instance by its **inverse distance (ID)** from the **test instance**:
    $w_j = \frac{1}{d_j + \epsilon}$

#### Ties for $K$-NN
In the case that we have an equal number of *votes* for a given instance we are trying to predict, we need a tie breaking mechanism:
- We can randomly break the tie by selecting a random class
- We can also take the class with the highest **prior** probability
- Or we can see if the addition of the $k+1$th instance breaks the tie

#### Choosing $K$
- Smaller values of $k$ tend to lead to lower classifier performance due to noise and overfitting
- Larger values of $k$ tend to drive the classifier performance toward a Zero-R performance 
- Use an odd value of $k$ to break ties 

#### Analysis of $K$-NN
A typical implementation involves a **brute-force computation** of distances between a test instance, and to every other training instance.
- For $N$ training instances, and $D$ dimensions, we end up with $O(DN)$ performance
- Although fast for small datasets, the method becomes infeasible as $N$ grows

Why is $k$-NN so slow?
- The model built by NB or a DT is generally much smaller than the number of training instances in the dataset:
    (Let $C$ be the number of classes, and $D$ the number of attributes:)
    - **Predicting** a test instance requires $O(CD)$ calculations for NB, and $O(D)$ node traversals for a DT
- The model built by $K$-NN$ is the dataset itself:
    - $k$-NN is lazy (everything is done at run time)
    - The time we save in training is lost if we have to make **several** predictions
    - Expensive index accessing
    - Prone to bias with an arbitrary $K$ value

## Lecture 8: Support Vector Machines (SVM):
#### Nearest Prototype Classification
- A parametric variance of the NN classification
- Instead of $k$-NN, we calculate the centroid of each class and use that to classify each test

#### SVM
A support vector machine is a non-probabilistic binary linear classifier.
- A linear hyperplane-based classifier for a two-class classification problem
- The particular hyperplane it selects is the **_maximum margin_** hyperplane
- A kernel function can be used to allow the SVM to find a non-linear separating boundary between two classes (transform data so that we can find a separating boundary)

#### Linear Classifiers
A separating hyperplane in $D$ dimensions can be defined by a normal $\mathbf{w} = <w_1,w_2,\dots,w_m>$ and intercept point $b = <x_1,x_2,\dots,x_m>$. 

The hyperplane equation is given as:

$\mathbf{w}\cdot \mathbf{x} + b = 0$

A linear classifier takes the form of (line in 2D, plane in 3D):

$f(x) = \mathbf{w}^T\mathbf{x} + b$

Given that a hyperplane exists, there are infinite number of solutions.

#### Margins
**Maximum Margin:**  
How can we rate the different decision boundaries to work out which is the "best"?
- For a given training set, we would like to find a decision boundary that allows us to make all correct and confident predictions on the training examples
- Some methods find a separating hyperplane, but not the optimal one (solution found but is it optimal?). SVM do find the optimal solution.
    - SVM maximizes the distance the hyperplane and the "difficult fringe points" which are close to the decision boundary
    - If there are no points near the decision surface, then there are no very uncertain classification decisions

**Soft Margin:**  
A possibly large margin solution is better even though constraints are being violated. This is the trade-off between the margin, and the number of mistakes on the training data. 

#### SVM-based Classification
- Associate one class as positive (+1), and one as negative (-1)
- Find the best hyperplane$\mathbf{w}$ and $b$, which maximise the margin between the positive and negative training instances (this is the **model**)
- To make a prediction for a test instance $\mathbf{t} = <t_1,t_2,\dots,t_m>$:
    - $f(t) = \mathbf{w}^\mathbf{t} + b$
    - Find $sign(f(t))$
    - Assign `?` to instances within the margin

#### Learning the SVM
For smaller training sets, we can use a naive training approach:
- Pick a plane $\mathbf{w}$ and $b$
- Find the worst classified sample $y_i$ (this is the expensive step for large datasets)
- Move plane $\mathbf{w}$ and/or $b$ to imrpove the classification of $y_i$
- Repeat until the algorithm converges to a solution

#### Kernel Function
To obtain a non-linear classifier, we can transform our data by applying a mapping function $\Phi$(i.e. log transform), and then apply a linear classifier to the new feature vectors.

#### Support Vectors
The objective is to find the data points that act as the **boundaries** of the two classes.
- These are referred to as the `support vectors` (although they are points that lie on the margin)
- They constrain the margin between the two classes

#### Optimisations
- We want to choose a plane $\mathbf{w}$ so that the margin $\frac{2}{||\mathbf{w}||}$ is maximised, given that all the points are on the correct side of the seperating hyperplane $y_k(\mathbf{w}^Tx_k + b) - 1 \geq 0$
- Since the partial derivatives to maximise $\frac{2}{||\mathbf{w}||}$ is inconvenient, we can instead minimise $\frac{1}{2}||\mathbf{w}||^2$

#### "Slack" (Allowing Soft Margins)
We can consider the case when the two classes are not (completely) linearly separable. We can introduce slack variables $\xi$ that allow a few points to be on the "wrong side" of the hyperplane at some cost $C$.

#### Constrained Optimisation Problems
Current state-of-the-art for solving constrained optimisation problems use the method of **Lagrange multipliers**, where we introduce a constant value $\alpha_k$ for each constraint.

The classification function then becomes:

$f(\mathbf{t}) = \sum^m_{i=1}\alpha_iy_i\mathbf{x}_i^T\mathbf{t} + b$

$b = y_j(1 - \xi_j) - \sum^m_{i=1}\alpha_iy_i\mathbf{x}_i^T\mathbf{x}_j$

Most of the Lagrange Multipliers $\alpha_k$ are 0, where the non-zero correspond to **support vectors**

#### Multiple Class SVM
Since SVM's are inherently two-class classifiers, most common approaches to extending to multiple classes include:
- One Verses All: classification chooses one class which classifies test data points with the greatest margin
- One Verses One: classification which chooses class selected by the most number of classifiers

#### SVM Analysis
- SVM's are a high-accuracy *margin classifier*
- Learning a model means finding the best separating hyperplane
- Classification is built on projection of a point onto a hyperplane normal
- SVM's have several parameters that need to be optimised and may be slow
- SVM's can be applied to non-linear data by using an appropriate *kernel function*

## Lecture 9: Discrete and Continuous Data
#### Types of Naive Bayes
- **Multivariate** NB: attributes are nominal, and can take any (fixed) number of values
- **Binomial** NB: attributes are binary (special case of multivariate)
- **Multinomial** NB: attributes are numbers (usually correspond to frequencies)
  - Probability distribution is constructed by considering the formula
  - $Pr(a_k = m | c_j) \approx Pr(a_k = 1 | c_j)^m/m!$
- **Gaussian** NB: attributes are real numbers
  - Instead of a PMF, we can use the PDF 

#### Decision Trees
To build a DT, we label a node with an attribute, and branches with corresponding attribute values. However, if the attribute(s) are numerical, then we can apply **Binarisation**:
- Each node is labelled with $a_k$, and has two branches: one branch is $a_k \leq m$, and the other branch is $a_k > m$
- Information Gain / Gain Ratio must be calculated for each non-trivial "split point" for each attribute
  - Naively, this is each unique attribute value in the dataset
  - Faster implementations will constrain the number of "split points" we need to consider
- Otherwise, this is the equivalent to an ID3 implementation
- Downside: may lead to arbitrarily large trees (we always want the smallest one)

#### Discretisation
Discretisation is the translation of continuous attributes onto nominal attributes (think _binning_). This process is usually performed in two steps:
1. Decide how many values to map the feature onto (equal-width, freqeuency)
2. Map the features onto $<(x_0,x_1],(x_1,x_2],\dots,(x_{n-1},x_n))>$

Although it is simple to implement and in most cases, a viable solution, we end up with loss of generality, no sense of "numeric proximity" / ordering, and may result in overfitting.

#### Unsupervised Discretisation
1. Partition the values into equal-width bins (equal intervals)
2. Sort the values and partition them into equal-sized bins (equal frequencies)
3. Apply a $k$-means clustering algorithm
   - Select $k$ points at random to act as seed clusters
   - Assign each instance to the cluster with the nearest centroid
   - Compute seed points as the centroids of the clusters of the current partition
   - Repeat until the assignment of instances to clusters becomes stable

#### Naive Supervised Discretisation
Idea: to "group" values into class-contiguous intervals
1. Sort values and identify breakpoints in class memberships

| 64  | 65 | 68  | 69  | 70  | 71 | 72 | 72  | 75  |
|-----|----|-----|-----|-----|----|----|-----|-----|
| yes | no | yes | yes | yes | no | no | yes | yes |

(64), (65), (68,69,70), (71,72), (72, 75)

2. Reposition any breakpoints where there is _no change_ in numerical value

| 64  | 65 | 68  | 69  | 70  | 71 | 72 | 72  | 75  |
|-----|----|-----|-----|-----|----|----|-----|-----|
| yes | no | yes | yes | yes | no | no | yes | yes |

(64), (65), (68,69,70), (71,72, 72), (75)

Although it is simple to implement, usually creates too many categories (overfitting). To combat this, we may apply the "group" values approach, but each category must have at least $n$ instances of a single class. 

## Lecture 10: Feature Selection
#### Wrapper Methods
Choose subsets of attributes that give the best performance on the development data (with respect to a single learner)
- Feature set will have optimal performance on development data
- Takes a very long time. For $m$ attributes we have $O(\frac{2^m}{6})$, so it is only practical for very small datasets

A **greedy approach** would be to train and evaluate the model on each single attribute. Then, we will choose the best attribute until it converges.
- Although it converges much quicker, it still follows an $O(\frac{1}{2}m^2)$ performance
- Usually converges to sub-optimal solutions (which we don't want)

The **ablation approach** will start with all attributes, then remove an attribute each iteration until it diverges.
- Assumes independence of attributes and takes $O(m^2)$ time

#### Embedded Methods
To some degree; SVM, Logistic Regression, and DT's perform some form of feature selection as part of the algorithm. These are what we refer to as **embedded methods**.

#### Filtering Methods (PMI, MI, and $\chi^2$)
Recall that if 2 events are independent, we have:

$Pr(A\cap B) = Pr(A)Pr(B)$.

Now we can calculate **Pointwise Mutual Information** (PMI):

$PMI(A=a \cup C=c) = log_2\bigg(\frac{Pr(A\cap c)}{Pr(A)Pr(c)}\bigg)$.

Attributes with the greatest PMI are most correlated with class. 


**CONTIGENCY TABLE - REFER TO SLIDES 56 - 66 STATISTICS MODULE 7**

**Mutual Information** can be calculated by:

$MI(A,C) = \sum_{i\in a,\bar{a}}\sum_{j \in c,\bar{c}}Pr(i,j)log_2\bigg(\frac{Pr(i\cap j)}{Pr(i)Pr(j)}\bigg)$

And the test statistic for the **$\chi^2$ distribution** is:

$Q = \sum_{i}\sum{j}\frac{(Y_{ij} - Y_iY_j/n)^2}{Y_iY_j/n} \sim \chi^2_{(r-1)(c-1)}$


