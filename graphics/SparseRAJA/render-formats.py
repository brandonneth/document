from plotnine import * 
import pandas as pd



general_matrix = [[0,0,0,1.1,0,0],[0,4.2,0,0,9.8,0],[2.6,0,2.4,3.7,0,6.0],[0,0,0,0,0,5.3],[0,0,0,0,0,0],[0,0,7.1,0,8.9,0]]
entries = []
for x in range(0,6):
  for y in range(0,6):
    #if general_matrix[x][y] != 0:
    entries += [(x,y,general_matrix[x][y])]
print(entries)



entries_df = pd.DataFrame(entries, columns=['i0','i1','val'])

dense_graphic = ggplot(entries_df, aes('factor(i0)','factor(i1)')) + scale_y_reverse()

dense_graphic += geom_tile(aes(width=0.95, height=0.95,fill='white')) 
dense_graphic += geom_text(aes(label='val'))

dense_graphic += theme(figure_size=(6,6))
dense_graphic.draw(show=True)