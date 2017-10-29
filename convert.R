library(rgl)
library(dplyr)

Lx=64
Ly=240
Lz=64

g = readSTL("os_test1.b.stl",plot=FALSE)

g %>% triangles3d()
writeSTL("test.stl")
cube3d() %>% translate3d(1,1,1) %>% scale3d(Lx/2,Ly/2,Lz/2) %>% shade3d(col=2,alpha=0.5)
snapshot3d("test.png")
writeWebGL("html")

f = function(x) as.integer(factor(round(x,4)))
gs = paste(f(g[,1]),f(g[,2]),f(g[,3]),sep=".")
gs = as.integer(factor(gs))
head(gs)
range(gs)

a = data.frame(gs=gs,i=1:nrow(g))

a = a[order(gs),]
i = a$i[!duplicated(a$gs)]

points = g[i,]
triangles = t(matrix(gs,3))
dim(points)
dim(triangles)
range(triangles)

collapsed = function(x) which(x[,1] == x[,2] | x[,1] == x[,3] | x[,2] == x[,3])
triangles = triangles[-collapsed(triangles),]

f = file("os_test1.msh","w")
cat("Triangles\n",file=f)
cat("3D-Nodes ",nrow(points),"\n",sep="",file=f)
i = 1:nrow(points)-1
write.table(cbind(i,i,0,points),file=f,row.names=FALSE,col.names=FALSE,sep="\t")
cat("\nTri3 ",nrow(triangles),"\n",file=f,sep="")
i = 1:nrow(triangles)-1
write.table(cbind(i,0,triangles-1),file=f,row.names=FALSE,col.names=FALSE,sep="\t")
close(f)
