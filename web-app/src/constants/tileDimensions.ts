/**
 * Tile dimension constants
 * These values are used in both TypeScript and CSS
 */

export const TILE_DIMENSIONS = {
  WIDTH: 52,
  HEIGHT: 70,
  X_OFFSET: 3,
  Y_OFFSET: 2,
  WIDTH_PX: '52px',
  HEIGHT_PX: '70px'
} as const;

// CSS variable names
export const CSS_VARIABLES = {
  TILE_WIDTH: '--tile-width',
  TILE_HEIGHT: '--tile-height'
} as const;

// Calculated values for background sprite sheet
export const BACKGROUND_DIMENSIONS = {
  WIDTH: TILE_DIMENSIONS.WIDTH * 9, // 9 tiles wide
  HEIGHT: TILE_DIMENSIONS.HEIGHT * 5, // 5 tiles tall
  WIDTH_PX: `${TILE_DIMENSIONS.WIDTH * 9}px`,
  HEIGHT_PX: `${TILE_DIMENSIONS.HEIGHT * 5}px`
} as const;

// Helper function to get CSS variable value
export const getCssVariableValue = (variableName: string): string => {
  return getComputedStyle(document.documentElement)
    .getPropertyValue(variableName)
    .trim();
};

// Helper function to get tile dimensions as numbers
export const getTileDimensions = () => ({
  width: TILE_DIMENSIONS.WIDTH,
  height: TILE_DIMENSIONS.HEIGHT
});

// Helper function to get background dimensions as numbers
export const getBackgroundDimensions = () => ({
  width: BACKGROUND_DIMENSIONS.WIDTH,
  height: BACKGROUND_DIMENSIONS.HEIGHT
});
