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
  # Iterate over each row in the game
  for i, line in enumerate(game):
    s = ""
    # Iterate over each number in the row
    for j, n in enumerate(line, 1):
      s += str(n) if n > 0 else " "
      s += " "
      # Add a vertical line every 3 numbers
      if j in [3, 6]:
        s += "| "
    # Add a horizontal line every 3 rows
    if i in [3, 6]:
      print("-" * 11 * 2)
    print(s)
  print()


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
  
  # Iterate over each cell in the game
  for i in range(9):
    for j in range(9):
      # If the cell is not empty, then we can skip it
      if game[i, j] > 0:
        continue

      # Get the row, column, and square of the cell
      row = game[i, :]
      column = game[:, j]
      sq = game[masks[(i // 3) * 3 + j // 3]]
      tmp = np.concatenate([row, column, sq])
      tmp = tmp[tmp > 0]
      tmp = np.unique(tmp)
      if tmp.size == 8:
        # find missing
        for target in range(1, 10):
          if target not in tmp:
            print(f'Found {target} to ({i + 1}, {j + 1}) index - by exclusion')
            return target, i, j
      elif tmp.size < 8: # multiple possibilities
        possible = [i for i in range(1, 10) if i not in tmp]
        for target in possible:
          mat = np.ones_like(game, dtype=np.bool_)
          mat[game > 0] = False
          for i_, j_ in zip(*np.where(game == target)):
            mat[i_, :] = False
            mat[:, j_] = False
            mat[masks[(i_ // 3) * 3 + j_ // 3]] = False
          
          for mask in masks:
            rows = (mat * mask).any(1)
            if rows.sum() == 1: # only a row
              mat[rows[:, None] * ~mask] = False # apply only outside the mask
            cols = (mat * mask).any(0)
            if cols.sum() == 1: # only a column
              mat[cols[None, :] * ~mask] = False

          if mat[i, j] == False:
            possible.remove(target)
            if i == 8:
              print(possible)
            if len(possible) == 1:
              value = possible[0]
              print(f'Found {value} to ({i + 1}, {j + 1}) index - by exclusion')
              return value, i, j


for _ in range(20):

  continue_loop = True
  while continue_loop:
    continue_loop = False
    for target in range(1, 10):
      while True:  
        result = find_move(game, target)
        if result is None:
          break
        continue_loop = True
        i, j = result
        game[i, j] = target
        print_board(game)

  # Find by exclusion
  result = find_by_exclusion(game)
  if result is None:
    break
  target, i, j = result
  game[i, j] = target
  print_board(game)

print("Final solution:")
print_board(game)


find_move(game, 1)