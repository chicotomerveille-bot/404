import React from "react";

/**
 * The 404 wordmark.
 *
 * The upstream script logotype is replaced by a plain typographic lockup:
 * the name set in the UI's own sans, tight and heavy, in the current text
 * colour. It inherits `currentColor`, so it flips with the theme without a
 * second asset — the point of a monochrome identity.
 */
const HandyTextLogo = ({
  width,
  height,
  className,
}: {
  width?: number;
  height?: number;
  className?: string;
}) => {
  return (
    <svg
      width={width}
      height={height}
      className={className}
      viewBox="0 0 930 328"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      role="img"
      aria-label="404"
    >
      <text
        x="465"
        y="248"
        textAnchor="middle"
        fill="currentColor"
        fontFamily="'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
        fontSize="300"
        fontWeight="700"
        letterSpacing="-12"
      >
        404
      </text>
    </svg>
  );
};

export default HandyTextLogo;
