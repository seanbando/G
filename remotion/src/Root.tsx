import React from "react";
import { Composition } from "remotion";
import { BridgeShort, BRIDGE_FRAMES } from "./videos/bridge/Bridge";
import { DollarShort, DOLLAR_FRAMES } from "./videos/dollar/Dollar";

export const Root: React.FC = () => (
  <>
    <Composition id="BridgeShort" component={BridgeShort} durationInFrames={BRIDGE_FRAMES} fps={30} width={1080} height={1920} />
    <Composition id="DollarShort" component={DollarShort} durationInFrames={DOLLAR_FRAMES} fps={30} width={1080} height={1920} />
  </>
);
