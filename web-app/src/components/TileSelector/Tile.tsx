import { type Tile as TileType } from '$/types/mahjong';
import { TILE_DIMENSIONS } from '$/constants/tileDimensions';
import styles from './Tiles.module.scss'

interface TileProps {
  tile: TileType;
  onClick: (tile: TileType) => void;
  className?: string;
}

export const Tile: React.FC<TileProps> = ({ tile, onClick, className }) => {
  const extraClass = tile.isFlower ? styles.flowerTile : tile.isHonor ? styles.honorTile : styles.suitTile
  return (
    <div
      className={`${styles.tile} ${extraClass} ${className}`}
      style={{
        width: TILE_DIMENSIONS.WIDTH_PX,
        height: TILE_DIMENSIONS.HEIGHT_PX,
        backgroundPosition: `-${tile.imgX * TILE_DIMENSIONS.WIDTH + TILE_DIMENSIONS.X_OFFSET}px -${tile.imgY * TILE_DIMENSIONS.HEIGHT + TILE_DIMENSIONS.Y_OFFSET}px`,
        backgroundSize: `${TILE_DIMENSIONS.WIDTH * 9}px ${TILE_DIMENSIONS.HEIGHT * 5}px`,
      }}
      onClick={() => onClick(tile)}
    />
  )
}
