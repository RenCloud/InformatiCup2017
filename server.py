import data.dataprep
import learning.frontend.Main

vec = dataprep.prep()
cat = Main.fit_rbm(vec)
