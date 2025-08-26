import type { Tile as TileType } from '$/types/mahjong'
import { Tile } from './Tile';
import { TILES } from '$/constants/tiles';
import styles from './Tiles.module.scss'

interface TileSelectorProps {
  onTileSelect: (tile: TileType) => void;
  onFlowerSelect: (flower: TileType) => void;
}

const TileSelector: React.FC<TileSelectorProps> = ({ onTileSelect, onFlowerSelect }) => {
  const handleTileClick = (tile: TileType) => {
    if (tile.isFlower) {
      onFlowerSelect(tile)
    } else {
      onTileSelect(tile)
    }
  }

  const groupTilesByCategory = () => {
    const grouped = {
      bamboos: TILES.filter(t => t.suit === 'B'),
      characters: TILES.filter(t => t.suit === 'C'),
      dots: TILES.filter(t => t.suit === 'D'),
      suits: TILES.filter(t => !t.isHonor && !t.isFlower),
      honors: TILES.filter(t => t.isHonor && !t.isFlower),
      flowers: TILES.filter(t => t.isFlower)
    }
    return grouped
  }

  const groupedTiles = groupTilesByCategory()

  return (
    <div className={styles.tileSelector}>
      <div className={styles.tileCategory}>
        <div className={styles.tileRow}>
          {groupedTiles.bamboos.map(tile => (
            <Tile
              key={tile.id}
              tile={tile}
              onClick={() => handleTileClick(tile)}
            />
          ))}
        </div>
        <div className={styles.tileRow}>
          {groupedTiles.characters.map(tile => (
            <Tile
              key={tile.id}
              tile={tile}
              onClick={() => handleTileClick(tile)}
            />
          ))}
        </div>
        <div className={styles.tileRow}>
          {groupedTiles.dots.map(tile => (
            <Tile
              key={tile.id}
              tile={tile}
              onClick={() => handleTileClick(tile)}
            />
          ))}
        </div>
      </div>

      <div className={styles.tileCategory}>
        <div className={styles.tileRow}>
          {groupedTiles.honors.map(tile => (
            <Tile
              key={tile.id}
              tile={tile}
              onClick={() => handleTileClick(tile)}
            />
          ))}
        </div>
      </div>

      <div className={styles.tileCategory}>
        <div className={styles.tileRow}>
          {groupedTiles.flowers.map(tile => (
            <Tile
              key={tile.id}
              tile={tile}
              onClick={() => handleTileClick(tile)}
            />
          ))}
        </div>
      </div>
    </div>
  )
}

export default TileSelector
