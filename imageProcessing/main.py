import detectAns

fileName = "research/"+"calibate__12.jpg" 
fileName_back = "research/"+"File02.png"

print(detectAns.frontDetect(fileName))
print(detectAns.backDetect(fileName_back))