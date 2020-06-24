library(arules)
mods <- read.transactions('~/PycharmProjects/mining_ml_repos/data/uniq_modules.csv', sep=',')
summary(mods)
itemFrequencyPlot(mods, type = 'absolute', topN = 50)
itms <- itemFrequency(mods, type = 'absolute')
itmsdf = data.frame(library = names(itms), frequency = itms)
row.names(itmsdf) <- NULL
colnames(itmsdf)
head(itmsdf)
Orditmsdf <- itmsdf[order(itmsdf$frequency, decreasing = TRUE),]
Orditmsdf <- Orditmsdf[Orditmsdf$frequency > 60,]
head(Orditmsdf)
write.csv(Orditmsdf, '~/PycharmProjects/mining_ml_repos/data/lib_frequency.csv', row.names = FALSE)
