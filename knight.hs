import System.Environment (getArgs)
import Data.Char (ord, chr)
import Data.List (minimumBy, (\\), intercalate, sort)
import Data.Ord (comparing)
 
type Square = (Int, Int)

boardSize = 5
 
board :: [Square]
board = [ (x,y) | x <- [1..boardSize], y <- [1..boardSize] ]
 
knightMoves :: Square -> [Square]
knightMoves (x,y) = filter (flip elem board) jumps
  where jumps = [ (x+i,y+j) | i <- jv, j <- jv, abs i /= abs j ]
        jv    = [1,-1,2,-2]
 
knightTour :: [Square] -> [Square]
knightTour moves
    | candMoves == [] = reverse moves
    | otherwise = knightTour $ newSquare : moves
  where newSquare = minimumBy (comparing (length . findMoves)) candMoves
        candMoves = findMoves $ head moves
        findMoves sq = knightMoves sq \\ moves
 
main :: IO ()
main = do
    --fmap  (putStrLn . head) getArgs
    sq <- fmap (toSq . head) getArgs
    printTour $ map toAlg $ knightTour [sq]
  where toAlg (x,y) = [chr (x + 96), chr (y + 48)]
        toSq [x,y] = ((ord x) - 96, (ord y) - 48)
        printTour [] = return ()
        printTour tour = do
            putStrLn $ intercalate " -> " $ take boardSize tour
            printTour $ drop boardSize tour