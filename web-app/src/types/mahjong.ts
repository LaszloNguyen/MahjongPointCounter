export interface Tile {
  id: string;
  suit: 'B' | 'C' | 'D' | 'W' | 'd' | 'F' | 'S';
  rank?: number;
  isHonor: boolean;
  isFlower: boolean;
  displayName: string;
  unicode?: string;
  imgX: number;
  imgY: number;
}

export interface Meld {
  id: string;
  type: 'chow' | 'pung' | 'kong' | 'chow2' | 'pung2' | 'kong2';
  tiles: Tile[];
  suit: string;
  rank?: number;
}

export interface HandState {
  handTiles: Tile[];
  meldedSets: Meld[];
  flowers: Tile[];
}

export interface PointResult {
  totalPoints: number;
  breakdown: {
    [key: string]: number;
  };
  description: string;
}
