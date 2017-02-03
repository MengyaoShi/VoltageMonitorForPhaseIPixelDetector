backer<-read.table('Readbacker_1283.dat')
naming<-read.table('naming.dat')
colnames(naming)[2]="ROC ID"
colnames(naming)[1]="Official.name.of.position"
backer$V_Digi<-2*1.235*backer$V2/backer$V5
backer$V_Ana<-2*1.235*backer$V3/backer$V5
colnames(backer)[1]="ROC ID"
backer<-merge(backer, naming, by="ROC ID")
plot(backer$V_Digi, ylim = c(2.5, 3.5)) 
plot(backer$V_Ana, ylim=c(1.8, 2.3))

plot(backer$V_Digi, backer$V_Ana, xlim=c(2.5, 3.5), ylim=c(1.7,2.3), xlab='Digital Votage', ylab='Analog Votage')
Id=0.46
Ia=0.4

perfect_digi_Vd = 3.5- Id*(0.97/2) - (Id+Ia)*(0.97/6)
lost_digi_Vd = 3.5 - Id*(0.97) - (Id+Ia)*(0.97/6)



perfect_ana_Vd = 2.4 - Id*(0.97/2) - (Id+Ia)*(0.97/6)

lost_ana_Vd = 2.4 - Id*(0.97) - (Id+Ia)*(0.97/6)

outlier_digi<-backer[which(backer$V_Digi<=lost_digi_Vd),]
outlier_ana<-backer[which(backer$V_Ana<=lost_ana_Vd),]
plot(outlier_ana$V_Ana)
plot(outlier_digi$`ROC ID`)
outlier_both<-backer[which(backer$V_Ana<=lost_ana_Vd & backer$V_Digi<=lost_digi_Vd),]
Serious_wrong<-backer[which(backer$V2>500| backer$V3>500),]

####
backer$Official.name.of.position<- sapply(backer$Official.name.of.position, as.character)
###
cableName_BmI<-read.csv('Cabling Map for FPix Phase 1 Detector - BmI.csv')
cableName_BpI<-read.csv('Cabling Map for FPix Phase 1 Detector - BpI.csv')
cableName_BmO<-read.csv('Cabling Map for FPix Phase 1 Detector - BmO.csv')
cableName_BpO<-read.csv('Cabling Map for FPix Phase 1 Detector - BpO.csv')
DCU<-read.csv('DCU.csv')
light_BmO<-cableName_BmO[,c(1,8,9)]
light_BmO<-na.omit(light_BmO)
light_BmO$isOdd<-light_BmO$PC.port%%2

light_BpI<-cableName_BpI[,c(1,8,9)]
light_BpI<-na.omit(light_BpI)
light_BpI$isOdd<-light_BpI$PC.port%%2

light_BpO<-cableName_BpO[,c(1,8,9)]
light_BpO<-na.omit(light_BpO)
light_BpO$isOdd<-light_BpO$PC.port%%2
light_BpO$Official.name.of.position<-paste(light_BpO$Official.name.of.position, "_ROC0", sep="")


merged<-merge(backer, light_BpO, all=TRUE, by="Official.name.of.position")

####Deal with DCU table

BmI_DCU<-DCU[,c(1:4)]
BpO_DCU<-DCU[,c(1, 5:8)]
BpI_DCU<-DCU[,c(1,9:12)]
BmO_DCU<-DCU[,c(1,13:16)]

Cleaned_BmI_DCU_p1<-BmI_DCU[c(1:26),]
colnames(Cleaned_BmI_DCU_p1)<-c("PC.position.Mirror","direct meas(V)","DCU meas(V)", "input(V)")
Cleaned_BmI_DCU_p1<-Cleaned_BmI_DCU_p1[c(3:26),]

Cleaned_BmI_DCU_p2<-BmI_DCU[c(29:54),]
colnames(Cleaned_BmI_DCU_p2)<-c("PC.position.Mirror","Va1 direct meas(V)","Va1 DCU meas(V)", "Va1 input(V)")
Cleaned_BmI_DCU_p2<-Cleaned_BmI_DCU_p2[c(3:26),]


Cleaned_BmI_DCU_p3<-BmI_DCU[c(57:82),]
colnames(Cleaned_BmI_DCU_p3)<-c("PC.position.Mirror","Vd1 direct meas(V)","Vd1 DCU meas(V)", "Vd1 input(V)")
Cleaned_BmI_DCU_p3<-Cleaned_BmI_DCU_p3[c(3:26),]


Cleaned_BmI_DCU_p4<-BmI_DCU[c(85:110),]
colnames(Cleaned_BmI_DCU_p4)<-c("PC.position.Mirror","Va2 direct meas(V)","Va2 DCU meas(V)", "Va2 input(V)")
Cleaned_BmI_DCU_p4<-Cleaned_BmI_DCU_p4[c(3:26),]

Cleaned_BmI_DCU_p5<-BmI_DCU[c(113:138),]
colnames(Cleaned_BmI_DCU_p5)<-c("PC.position.Mirror","Vd2 direct meas(V)","Vd2 DCU meas(V)", "Vd2 input(V)")
Cleaned_BmI_DCU_p5<-Cleaned_BmI_DCU_p5[c(3:26),]

Cleanned_BmI_DCU<-merge(merge(merge(merge(Cleaned_BmI_DCU_p1, Cleaned_BmI_DCU_p2, by="PC.position.Mirror"), Cleaned_BmI_DCU_p3, by='PC.position.Mirror'), Cleaned_BmI_DCU_p4, by='PC.position.Mirror'), Cleaned_BmI_DCU_p5, by='PC.position.Mirror')

###DCU PbO##
Cleaned_BpO_DCU_p1<-BpO_DCU[c(1:26),]
BpO_name<-sapply(BpO_DCU[2,], as.character)

BpO_name[1]<-"PC.position.Mirror"
colnames(Cleaned_BpO_DCU_p1)<-BpO_name
Cleaned_BpO_DCU_p1<-Cleaned_BpO_DCU_p1[c(3:26),]

Cleaned_BpO_DCU_p2<-BpO_DCU[c(29:54),]
BpO_name<-sapply(BpO_DCU[2,], as.character)
BpO_name[1]<-"PC.position.Mirror"
BpO_name[2:5]<-paste('Va1',BpO_name[2:5])
colnames(Cleaned_BpO_DCU_p2)<-BpO_name
Cleaned_BpO_DCU_p2<-Cleaned_BpO_DCU_p2[c(3:26),]


Cleaned_BpO_DCU_p3<-BpO_DCU[c(57:82),]
BpO_name<-sapply(BpO_DCU[2,], as.character)
BpO_name[1]<-"PC.position.Mirror"
BpO_name[2:5]<-paste('Vd1',BpO_name[2:5])
colnames(Cleaned_BpO_DCU_p3)<-BpO_name
Cleaned_BpO_DCU_p3<-Cleaned_BpO_DCU_p3[c(3:26),]


Cleaned_BpO_DCU_p4<-BpO_DCU[c(85:110),]
BpO_name<-sapply(BpO_DCU[2,], as.character)
BpO_name[1]<-"PC.position.Mirror"
BpO_name[2:5]<-paste('Va2',BpO_name[2:5])
colnames(Cleaned_BpO_DCU_p4)<-BpO_name
Cleaned_BpO_DCU_p4<-Cleaned_BpO_DCU_p4[c(3:26),]

Cleaned_BpO_DCU_p5<-BpO_DCU[c(113:138),]
BpO_name<-sapply(BpO_DCU[2,], as.character)
BpO_name[1]<-"PC.position.Mirror"
BpO_name[2:5]<-paste('Vd2',BpO_name[2:5])
colnames(Cleaned_BpO_DCU_p5)<-BpO_name
Cleaned_BpO_DCU_p5<-Cleaned_BpO_DCU_p5[c(3:26),]

Cleanned_BpO_DCU<-merge(merge(merge(merge(Cleaned_BpO_DCU_p1, Cleaned_BpO_DCU_p2, by="PC.position.Mirror"), Cleaned_BpO_DCU_p3, by='PC.position.Mirror'), Cleaned_BpO_DCU_p4, by='PC.position.Mirror'), Cleaned_BpO_DCU_p5, by='PC.position.Mirror')


#BpI#

Cleaned_BpI_DCU_p1<-BpI_DCU[c(1:26),]
BpI_name<-sapply(BpI_DCU[2,], as.character)
BpI_name[1]<-"PC.position.Mirror"
colnames(Cleaned_BpI_DCU_p1)<-BpI_name
Cleaned_BpI_DCU_p1<-Cleaned_BpI_DCU_p1[c(3:26),]

Cleaned_BpI_DCU_p2<-BpI_DCU[c(29:54),]
BpI_name<-sapply(BpI_DCU[2,], as.character)
BpI_name[1]<-"PC.position.Mirror"
BpI_name[2:5]<-paste('Va1',BpI_name[2:5])
colnames(Cleaned_BpI_DCU_p2)<-BpI_name
Cleaned_BpI_DCU_p2<-Cleaned_BpI_DCU_p2[c(3:26),]


Cleaned_BpI_DCU_p3<-BpI_DCU[c(57:82),]
BpI_name<-sapply(BpI_DCU[2,], as.character)
BpI_name[1]<-"PC.position.Mirror"
BpI_name[2:5]<-paste('Vd1',BpI_name[2:5])
colnames(Cleaned_BpI_DCU_p3)<-BpI_name
Cleaned_BpI_DCU_p3<-Cleaned_BpI_DCU_p3[c(3:26),]


Cleaned_BpI_DCU_p4<-BpI_DCU[c(85:110),]
BpI_name<-sapply(BpI_DCU[2,], as.character)
BpI_name[1]<-"PC.position.Mirror"
BpI_name[2:5]<-paste('Va2',BpI_name[2:5])
colnames(Cleaned_BpI_DCU_p4)<-BpI_name
Cleaned_BpI_DCU_p4<-Cleaned_BpI_DCU_p4[c(3:26),]

Cleaned_BpI_DCU_p5<-BpI_DCU[c(113:138),]
BpI_name<-sapply(BpI_DCU[2,], as.character)
BpI_name[1]<-"PC.position.Mirror"
BpI_name[2:5]<-paste('Vd2',BpI_name[2:5])
colnames(Cleaned_BpI_DCU_p5)<-BpI_name
Cleaned_BpI_DCU_p5<-Cleaned_BpI_DCU_p5[c(3:26),]

Cleanned_BpI_DCU<-merge(merge(merge(merge(Cleaned_BpI_DCU_p1, Cleaned_BpI_DCU_p2, by="PC.position.Mirror"), Cleaned_BpI_DCU_p3, by='PC.position.Mirror'), Cleaned_BpI_DCU_p4, by='PC.position.Mirror'), Cleaned_BpI_DCU_p5, by='PC.position.Mirror')

#BmO##
Cleaned_BmO_DCU_p1<-BmO_DCU[c(1:26),]
BmO_name<-sapply(BmO_DCU[2,], as.character)
BmO_name[1]<-"PC.position.Mirror"
colnames(Cleaned_BmO_DCU_p1)<-BmO_name
Cleaned_BmO_DCU_p1<-Cleaned_BmO_DCU_p1[c(3:26),]

Cleaned_BmO_DCU_p2<-BmO_DCU[c(29:54),]
BmO_name<-sapply(BmO_DCU[2,], as.character)
BmO_name[1]<-"PC.position.Mirror"
BmO_name[2:5]<-paste('Va1',BmO_name[2:5])
colnames(Cleaned_BmO_DCU_p2)<-BmO_name
Cleaned_BmO_DCU_p2<-Cleaned_BmO_DCU_p2[c(3:26),]


Cleaned_BmO_DCU_p3<-BmO_DCU[c(57:82),]
BmO_name<-sapply(BmO_DCU[2,], as.character)
BmO_name[1]<-"PC.position.Mirror"
BmO_name[2:5]<-paste('Vd1',BmO_name[2:5])
colnames(Cleaned_BmO_DCU_p3)<-BmO_name
Cleaned_BmO_DCU_p3<-Cleaned_BmO_DCU_p3[c(3:26),]


Cleaned_BmO_DCU_p4<-BmO_DCU[c(85:110),]
BmO_name<-sapply(BmO_DCU[2,], as.character)
BmO_name[1]<-"PC.position.Mirror"
BmO_name[2:5]<-paste('Va2',BmO_name[2:5])
colnames(Cleaned_BmO_DCU_p4)<-BmO_name
Cleaned_BmO_DCU_p4<-Cleaned_BmO_DCU_p4[c(3:26),]

Cleaned_BmO_DCU_p5<-BmO_DCU[c(113:138),]
BmO_name<-sapply(BmO_DCU[2,], as.character)
BmO_name[1]<-"PC.position.Mirror"
BmO_name[2:5]<-paste('Vd2',BmO_name[2:5])
colnames(Cleaned_BmO_DCU_p5)<-BmO_name
Cleaned_BmO_DCU_p5<-Cleaned_BmO_DCU_p5[c(3:26),]

Cleanned_BmO_DCU<-merge(merge(merge(merge(Cleaned_BmO_DCU_p1, Cleaned_BmO_DCU_p2, by="PC.position.Mirror"), Cleaned_BmO_DCU_p3, by='PC.position.Mirror'), Cleaned_BmO_DCU_p4, by='PC.position.Mirror'), Cleaned_BmO_DCU_p5, by='PC.position.Mirror')


####
merged$PC.position.Mirror<-sapply(merged$PC.position.Mirror, as.character)
#print(merged$PC.position.Mirror)
for(i in 1:length(merged$PC.position.Mirror)) {
  if (!is.na(merged$PC.position.Mirror[i])) {
    a=merged$PC.position.Mirror[i]
    merged$PC.position.Mirror[i]<- paste(substr(a, start=2, stop=2), substr(a, start=1, stop=1), substr(a, start=3, stop = 3), sep="")
  }
}
#print(merged$PC.position.Mirror)
Cleanned_BpO_DCU$PC.position.Mirror<-sapply(Cleanned_BpO_DCU$PC.position.Mirror, as.character)
Everything<-merge(merged, Cleanned_BpO_DCU, by="PC.position.Mirror", all=TRUE)

##If PC.port is odd, then set Va1 Vd1 and Va_final Vd_final, otherwise set Va2 Vd2 as Va_final Vd_final
Everything<-Everything[1:168,]
Everything$`Va1 direct meas. (V)`<- as.numeric(levels(Everything$`Va1 direct meas. (V)`))[Everything$`Va1 direct meas. (V)`]
Everything$`Va2 direct meas. (V)`<-as.numeric(levels(Everything$`Va2 direct meas. (V)`))[Everything$`Va2 direct meas. (V)`]
for( i in 1:length(Everything$isOdd)){
  if(Everything$isOdd[i]){
    Everything$`Va_final direct meas. (V)`[i]<-Everything$`Va1 direct meas. (V)`[i]
  }
  else{
    Everything$`Va_final direct meas. (V)`[i]<-Everything$`Va2 direct meas. (V)`[i]
  }
}

##Same thing for non direct meas, 
Everything$`Va1 DCU* meas. (V)`<-as.numeric(levels(Everything$`Va1 DCU* meas. (V)`))[Everything$`Va1 DCU* meas. (V)`]
Everything$`Va2 DCU* meas. (V)`<-as.numeric(levels(Everything$`Va2 DCU* meas. (V)`))[Everything$`Va1 DCU* meas. (V)`]
for( i in 1:length(Everything$isOdd)){
  if(Everything$isOdd[i]){
    Everything$`Va_final DCU* meas. (V)`[i] <-Everything$`Va1 DCU* meas. (V)`[i]
  }
  else{
    Everything$`Va_final DCU* meas. (V)`[i]<-Everything$`Va2 DCU* meas. (V)`[i]
  }
}

## same thing for digi
Everything<-Everything[1:168,]
Everything$`Vd1 direct meas. (V)` <- as.numeric(levels(Everything$`Vd1 direct meas. (V)`))[Everything$`Vd1 direct meas. (V)`]
Everything$`Vd2 direct meas. (V)` <-as.numeric(levels(Everything$`Vd2 direct meas. (V)`))[Everything$`Vd2 direct meas. (V)`]
for( i in 1:length(Everything$isOdd)){
  if(Everything$isOdd[i]){
    Everything$`Vd_final direct meas. (V)`[i]<-Everything$`Vd1 direct meas. (V)`[i]
  }
  else{
    Everything$`Vd_final direct meas. (V)`[i]<-Everything$`Vd2 direct meas. (V)`[i]
  }
}

Everything$`Vd1 DCU* meas. (V)`<-as.numeric(levels(Everything$`Vd1 DCU* meas. (V)`))[Everything$`Vd1 DCU* meas. (V)`]
Everything$`Vd2 DCU* meas. (V)`<-as.numeric(levels(Everything$`Vd2 DCU* meas. (V)`))[Everything$`Vd2 DCU* meas. (V)`]
for( i in 1:length(Everything$isOdd)){
  if(Everything$isOdd[i]){
    Everything$`Vd_final DCU* meas. (V)`[i] <-Everything$`Vd1 DCU* meas. (V)`[i]
  }
  else{
    Everything$`Vd_final DCU* meas. (V)`[i]<-Everything$`Vd2 DCU* meas. (V)`[i]
  }
}

##Plot difference answer Will's first question

Everything$`Diff_Vd_DCU* means. (V)`<-(Everything$`Vd_final DCU* meas. (V)`-Everything$V_Digi)
Everything$`Diff_Va_DCU* means. (V)`<-(Everything$`Va_final DCU* meas. (V)`-Everything$V_Ana)
write.table(Everything, file='everything.csv')
plot(Everything$`ROC ID`,Everything$`Diff_Vd_DCU* means. (V)`, xlab='ROC ID', ylab='Voltage drop between portcard voltage and module, Vd(V)')
