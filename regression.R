rm(list = ls())
# 使用图形窗口
dev.off()


#install.packages("forecast")
library(forecast)
#install.packages("stargazer")
library(stargazer)
#install.packages("psych")
library(psych)
library(corrplot)

yelp.df = read.csv("D:/论文记录/shuju/data.csv")


yelp.df$has_profile <- 1 - yelp.df$has_profile
yelp.df$non_recommend <- yelp.df$fake

yelp.df$rest_review_count <- yelp.df$total_review_count
yelp.df$user_friend_count <- yelp.df$friend
yelp.df$user_review_count <- yelp.df$review
yelp.df$rating_1 <- yelp.df$X1
yelp.df$rating_2 <- yelp.df$X2
yelp.df$rating_4 <- yelp.df$X4
yelp.df$rating_5 <- yelp.df$X5

#model 1
selected_data1 <- yelp.df[, c('rating_dev','word_count',
                              'adj_POS', 'verb_POS', 'adv_POS',  
                              'past_tense','present_tense', 'future_tense',
                              'neutral',
                              'rest_review_count','point',
                              'user_friend_count', 'user_review_count', 'has_profile',
                              'fake')]
yelp.glm1 = glm(fake ~ ., data = selected_data1, family = "binomial")
summary(yelp.glm1)

#model 2
selected_data2 <- yelp.df[, c('rating_dev','word_count',
                              'adj_POS', 'verb_POS', 'adv_POS',  
                              'past_tense','present_tense', 'future_tense',
                              'positive','negative',
                              'rest_review_count','point',
                              'user_friend_count', 'user_review_count', 'has_profile',
                              'fake')]
yelp.glm2 = glm(fake ~ ., data = selected_data2, family = "binomial")
summary(yelp.glm2)


#model 3
selected_data3 <- yelp.df[, c( 'rating_5', 'rating_4', 'rating_2', 'rating_1','word_count',
                              'adj_POS', 'verb_POS', 'adv_POS',  
                              'past_tense','present_tense', 'future_tense',
                              'neutral',
                              'rest_review_count','point',
                              'user_friend_count', 'user_review_count', 'has_profile',
                              'fake')]
yelp.glm3 = glm(fake ~ ., data = selected_data3, family = "binomial")
summary(yelp.glm3)




# 使用 stargazer 输出 HTML 表格
html_table1 <- stargazer(yelp.glm1, type = "html", title = "Model 3", single.row = TRUE)
html_table2 <- stargazer(yelp.glm2, type = "html", title = "Model 1", single.row = TRUE)
html_table3 <- stargazer(yelp.glm3, type = "html", title = "Model 2", single.row = TRUE)

# 创建一个 HTML 文件
html_file_path <- "C:/Users/10047/Documents/yelp.glm.html"
cat("<html><head><style>table {float: left; margin-right: 10px;}</style></head><body>", file = html_file_path)

# 将表格嵌套到 HTML 文件中
cat(html_table2, file = html_file_path, append = TRUE)
cat(html_table3, file = html_file_path, append = TRUE)
cat(html_table1, file = html_file_path, append = TRUE)

# 关闭 HTML 文件
cat("</body></html>", file = html_file_path, append = TRUE)


