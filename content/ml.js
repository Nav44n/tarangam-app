// Tarangam — KTU 2024 scheme, S5 CSE
// FILE: content/ml.js (Skeleton & Registry)

window.SUBJECTS = {
  ml: {
    key: "ml",
    name: "Machine Learning",
    code: "PCCST503",
    credits: 3,
    modules: [
      { num: 1, title: "Introduction to ML & Regression", hours: 9, topics: [] },
      { num: 2, title: "Classification & Generalisation", hours: 9, topics: [] },
      { num: 3, title: "SVM & Neural Networks", hours: 9, topics: [] },
      { num: 4, title: "Unsupervised Learning", hours: 9, topics: [] }
    ]
  }
};

// Helper function: Individual topic files will use this to inject themselves into the app
window.addTopic = function(moduleNum, topicData) {
  var mod = window.SUBJECTS.ml.modules.find(function(m) { return m.num === moduleNum; });
  if (mod) {
    mod.topics.push(topicData);
  } else {
    console.error("Module " + moduleNum + " not found for topic: " + topicData.title);
  }
};