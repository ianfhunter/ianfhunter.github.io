---
author: ianfhunter
category: 1 technical
math: true
mermaid: true
share: true
tag: writing
---

# Detecting Spam on Hacktoberfest

Spam PRs are a plague for Hacktoberfest, with people from around the world trying to make PRs, ANY PRS! to get their hands on the exclusive tshirts.

Using the [guide here](https://towardsdatascience.com/nlp-spam-detection-in-sms-text-data-using-deep-learning-b8632db85cc8) I trained a neural network from the [HackSquad](https://www.hacksquad.dev/) API which has moderators manually marking spam PRs.

Using a Dense Neural Network was just about as effective as either an LSTM or a Bidirectional LSTM which surprised me, and it was also decently faster.

Overall, each method was about 65-70% accurate. 

Here are some individual classifications:

<img src='/assets/img/notes/Pasted image 20221025173523.png' />

Because there are two classes, anything >50% is considered spam.  With the (relatively) low correctness, I think better results may be gathered if spam alerts were labelled at say 75% confidence and above.

My next step is to get more meta information involved in the training. Using the [Github API](https://docs.github.com/en/rest/pulls) I intend to gather details like the numbers of lines changed and perhaps also whether the contributor also owns the repository.

One potential issue stopping us from achieving high rates of accuracy is that classifying a PR as spam is not always clear-cut - and there are many items in the dataset that are either falsely labelled spam or slipped through the gaps. As HackSquad continues, the labelling will surely become more precise.