library(arules)
mods <- read.transactions('~/PycharmProjects/mining_ml_repos/data/uniq_modules.csv', sep=',')
summary(mods)
itemFrequencyPlot(mods, type = 'absolute', topN = 50)
itms <- itemFrequency(mods, type = 'absolute')
itmsdf = data.frame(library = names(itms), frequency = itms)
row.names(itmsdf) <- NULL
colnames(itmsdf)
head(itmsdf)
itmsdf[order(itmsdf$frequency, decreasing = TRUE),]

