### Profile表：用于存储用户信息

+ user属性与Django的默认User建立一一对应关系，Django默认User有username，password，email，first_name，last_name属性

### ToLearn表：用于存储用户正在学习的教程

+ user属性外码参照于Profile表的id
+ course属性外码参照于Course表的id
+ lesson_num属性表示学到了第几节

### HaveLearned表：用户存储用户已经学过的课程

+ user属性外码参照于Profile表的id
+ course属性外码参照于Course表的id

### Course表：用于存储某个教程的基本信息

+ course_name
+ brief属性即每一个教程一两句话的简单介绍
+ overview属性即codecademy中每个教程的overview
+ classification属性表示教程所属类别
+ release_date属性表示教程的发布日期
+ course_auth属性表示教程的作者
+ total_lesson属性表示lesson数

### Lesson表：用于存储某个教程中的一节，即一个网页上的内容

+ course属性外码参照于Course表的id，用于建立lesson与所属course的联系


+ lesson_title
+ lesson_num属性表示该lesson是教程中的第几节
+ learn属性对应于codecademy中的learn，即知识点或知识点和问题
+ instructions属性对应于codecademy中的instructions，即需要做的步骤或实现思路
+ hint属性对应于codecademy中的hint


+ language属性表示该节所用编程语言
+ inputfile属性表示问题用输入（如果需要）
+ outputfile属性表示问题的标准输出

### Submission表：用于表示用户的一次提交

+ lesson属性外码参照于Lesson表的id
+ submission_time属性表示提交的时间
+ submitter属性外码参照于Profile表示提交者
+ code属性表示提交的代码
+ status表示本次提交的结果
+ result表示本次提交的输出

