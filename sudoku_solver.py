import numpy as np

# mockup
game = [
  [0,0,0, 0,0,0, 0,0,0],
  [0,0,0, 0,0,0, 0,0,0],
  [0,0,0, 0,0,0, 0,0,0],

  [0,0,0, 0,0,0, 0,0,0],
  [0,0,0, 0,0,0, 0,0,0],
  [0,0,0, 0,0,0, 0,0,0],

  [0,0,0, 0,0,0, 0,0,0],
  [0,0,0, 0,0,0, 0,0,0],
  [0,0,0, 0,0,0, 0,0,0]
]

game = [
  [0,0,0, 0,5,3, 9,0,0],
  [0,0,0, 8,9,0, 7,3,0],
  [0,0,0, 0,0,0, 0,8,0],

  [0,0,5, 0,4,8, 0,0,2],
  [0,0,0, 6,0,0, 0,0,0],
  [0,1,0, 0,0,5, 0,0,0],

  [0,0,8, 0,0,0, 0,0,4],
  [0,5,4, 7,0,0, 6,0,0],
  [0,0,2, 1,3,0, 0,9,0]
]

def print_board(game):
  for i, line in enumerate(game):
    s = ""
    for j, n in enumerate(line, 1):
      s += str(n) if n > 0 else " "
      s += " "
      if j in [3, 6]:
        s += "| "
    if i in [3, 6]:
      print("-" * 11 * 2)
    print(s)


game = np.array(game)

print_board(game)

# setting masks array
masks = np.zeros((9, 9, 9), dtype=np.bool_)
for i in range(3):
  for j in range(3):
    masks[i * 3 + j][i * 3: i * 3 + 3, j * 3: j * 3 + 3] = True


def find_move(game, target):

  mat = np.ones_like(game, dtype=np.bool_)
  mat[game > 0] = False
  for i, j in zip(*np.where(game == target)):
    mat[i, :] = False
    mat[:, j] = False
    mat[masks[(i // 3) * 3 + j // 3]] = False
    
  if (~mat).all():
    # print("All solutions found")
    return 
  
  for mask in masks:
    rows = (mat * mask).any(1)
    if rows.sum() == 1: # only a row
      mat[rows[:, None] * ~mask] = False # apply only outside the mask
    cols = (mat * mask).any(0)
    if cols.sum() == 1: # only a column
      mat[cols[None, :] * ~mask] = False
  
  for mask in masks:
    if mat[mask].sum() == 1:
      i, j = np.where(mat * mask)
      i, j = i[0], j[0]
      # game[i, j] = target
      print(f'Found {target} to ({i + 1}, {j + 1}) index')
      return i, j
  
  # print("No closed solution found")
  
def find_by_exclusion(game):
  for i in range(9):
    for j in range(9):
      if game[i, j] > 0:
        continue
      row = game[i, :]
      column = game[:, j]
      sq = game[masks[(i // 3) * 3 + j // 3]]
      tmp = np.concatenate([row, column, sq])
      tmp = tmp[tmp > 0]
      tmp = np.unique(tmp)
      if tmp.size == 8:
        # find missing
        for k in range(1, 10):
          if k not in tmp:
            print(f'Found {k} to ({i + 1}, {j + 1}) index - by exclusion')
            return k, i, j

solutions = 0
for _ in range(20):

  for target in range(1, 10):
    while True:  
      result = find_move(game, target)
      if result is None:
        break
      solutions += 1
      i, j = result
      game[i, j] = target   

  while True:
    result = find_by_exclusion(game)
    if result is None:
      break
    target, i, j = result
    game[i, j] = target

print(f'Found {solutions} solutions')
print_board(game)


find_move(game, 1)