# slimme meter data vezel 14

# postgreSQL
require("RPostgreSQL", lib.loc="~/R/x86_64-pc-linux-gnu-library/3.0")

# Establish connection to PoststgreSQL using RPostgreSQL
drv <- dbDriver("PostgreSQL")

# read P1 data from P1DB
# Full version of connection setting
con <- dbConnect(drv, dbname="p1db",host="localhost",port=5432,user="hugo",password="snampook" )
#conPi <- dbConnect(drv, dbname="p1db",host="raspberrypi",port=5432,user="hugo",password="snampook" )

# read table as dataframe
df.p1 <- dbReadTable(con, c("p1data"))

#read the aggregated view per 24 hours
df.gas <- dbReadTable(con, c("vw_gpd"))
names(df.gas)
# remove first line as it contains absolute ytd gas usage
df.gas <- df.gas[-1,]
# shift one hour
dt <- as.POSIXlt(df.gas$dt)
dt$hour <- as.POSIXlt(df.gas$dt)$hour -2
df.gas$dt <- dt

# transform UTC naar datetime
df.p1$dt <- as.POSIXlt(df.p1$utc_timestamp, origin="1970-01-01", tz="") # current timezone

# add day of week
df.gas$day <- weekdays(strptime(df.gas$dt, "%Y-%m-%d"))
df.p1$day <- weekdays(strptime(df.p1$dt, "%Y-%m-%d"))

# add hour from timestamp
df.gas$hour <- strptime(df.gas$dt,"%Y-%m-%d %H:%M:%S")$hour
df.p1$hour <- strptime(df.p1$dt,"%Y-%m-%d %H:%M:%S")$hour

# ggplot
require(ggplot2)

# # some plots on gas usage
# ggplot(df.gas, aes(dt, dg)) + geom_line() + xlab("") + ylab("Gas use per hour")
# 
# # aggregate per day of the week
# boxplot(df.gas$dg ~ df.gas$day)
# 
# # aggregate gas per hour
# res1 <- aggregate(dg ~ hour , data=df.gas, FUN=sum)
# plot(res1,main="Gas use per hour of day")
# 
# # aggregate electra per hour
# # TODO check mean or sum ...
# res3 <- aggregate(afgenomen_vermogen ~ hour , data=df.p1, FUN=mean)
# plot(res3,main="Power use per hour of day")
# 
# # gas per day of the week per hour
# res2 <- aggregate(dg ~ day + hour , data=df.gas, FUN=mean)
# ggplot(res2, aes(hour, dg)) + geom_point() + xlab("") +
#   ylab("Average gas use per hour") + facet_grid(day ~ .) + stat_smooth(method = "auto", span = 0.25)
# 
# # electra per day of the week per hour
# res4 <- aggregate(afgenomen_vermogen ~ day + hour , data=df.p1, FUN=sum)
# ggplot(res4, aes(hour, afgenomen_vermogen)) + geom_point() + xlab("") +
#   ylab("Average power use per hour") + facet_grid(day ~ .) + stat_smooth(method = "auto", span = 0.25)
# 
# 
# g <- ggplot(df.gas, aes(hour, dg))
# g + geom_point() + xlab("") + ylab("Gas use per hour") + facet_grid(day ~ .) + geom_smooth(method = "auto", size = 1.5)

# Close PostgreSQL connection 
dbDisconnect(con)

# read weather Data from wsdb
conWS <- dbConnect(drv, dbname="wsdb",host="localhost",port=5432,user="hugo",password="snampook" )

# read table as dataframe
df.ti <- dbReadTable(conWS, c("intempdata"))
df.to <- dbReadTable(conWS, c("outtempdata"))
# Close PostgreSQL connection 
dbDisconnect(conWS)

# convert timestamp to POSIX
df.ti$dt <- as.POSIXlt(df.ti$utc_timestamp, origin="1970-01-01", tz="") #timezone

# aggregate per hour
intemp <- setNames(aggregate(intemp ~ cut(dt, 'hours'), data=df.ti, mean),c("dt","intemp"))
inhumidity <- setNames(aggregate(inhumidity ~ cut(dt, 'hours'), data=df.ti, mean),c("dt","inhumidity"))

# set dt back to posix apparently aggregate cuts them to factors
intemp$dt <- as.POSIXct(intemp$dt)
inhumidity$dt <- as.POSIXct(inhumidity$dt)

# merge
df.ti.h <- merge(intemp,inhumidity, by=1)

# add day of week
df.ti.h$day <- weekdays(strptime(df.ti.h$dt, "%Y-%m-%d"))
# add hour from timestamp
df.ti.h$hour <- strptime(df.ti.h$dt,"%Y-%m-%d %H:%M:%S")$hour

# convert timestamp to POSIX
df.to$dt <- as.POSIXlt(df.to$utc_timestamp, origin="1970-01-01", tz="CET")

# aggregate per hour
outtemp <- setNames(aggregate(outtemp ~ cut(dt, 'hours'), data=df.to, mean),c("dt","outtemp"))
outhumidity <- setNames(aggregate(outhumidity ~ cut(dt, 'hours'), data=df.to, mean),c("dt","outhumidity"))
# set dt back to posix apparently aggregate cuts them to factors
outtemp$dt <- as.POSIXct(outtemp$dt)
outhumidity$dt <- as.POSIXct(outhumidity$dt)

# merge
df.to.h <- merge(outtemp,outhumidity, by=1)
# merge inside and outside datasets
df.t <- merge(df.ti.h,df.to.h, by=1)
# calc delta temp
df.t$dtemp <- df.t$intemp-df.t$outtemp
# # plot hist
# hist(df.t$dtemp, breaks=100)
# hist(df.tot$dg, breaks=100)
# hist(df.t$intemp, breaks=100)

# combine p1 gas  and weatherdata
df.tot <- merge(df.t,df.gas)

# # plot 
# plot(df.tot$dtemp,df.tot$dg)
# plot(df.tot$outtemp,df.tot$dg)
# plot(df.tot$intemp,df.tot$dg)

# correlation between temps humidity and gas
df.num <- df.tot[,c("intemp","outtemp","dg","dtemp","inhumidity","outhumidity")]
# correlation
cor(df.num)

# filter on if we burn gas
df <- df.num[df.num$dg>0,]

cor(df$dg,df$dtemp)
plot(df$dg,df$dtemp)

# # fit model
# m1 <- glm(dg ~ dtemp + outtemp + outhumidity, data=df.tot)
# m1b <- glm(dg ~ dtemp + outtemp + outhumidity, data=df)
# m2 <- glm(dtemp ~ dg + outtemp + outhumidity, data=df.tot)

# plot specific date
df.date <- df.tot[as.Date(df.tot$dt) %in% as.Date(c("2014-01-05")),]

barplot(df.date$dg)

ggplot(df.date, aes(x=dt,y=dg)) + geom_bar(stat="identity")

# melt all temps
library("reshape2")
mdf <- melt(df.date[c("dt","intemp","outtemp","dtemp")], id.vars="dt", value.name="value", variable.name="temp")

p1 <- ggplot(data=mdf, aes(x=dt, y=value, group = temp, colour = temp)) +
  geom_line() +
  geom_point( size=4, shape=21, fill="white") +
  ylab("Temperatuur (C)") + xlab(" ") + 
  guides(colour=FALSE)

p2 <- ggplot(df.date, aes(x=dt,y=dg)) + 
  ylab("Gasverbruik") + xlab("Tijdstip") + 
  geom_bar(stat="identity")

require(gridExtra)
grid.arrange(p1, p2)

