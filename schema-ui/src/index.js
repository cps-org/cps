import React from 'react';
import ReactDOM from 'react-dom/client';
import { JsonSchemaViewer } from "@stoplight/json-schema-viewer";
import schema from './cps.schema.json';
import { Provider as MosaicProvider } from '@stoplight/mosaic';
import { injectStyles } from '@stoplight/mosaic';

const root = ReactDOM.createRoot(document.getElementById('root'));
injectStyles();
root.render(
  <React.StrictMode>
    <MosaicProvider>
      <JsonSchemaViewer
        name="CPS"
        schema={schema}
        expanded={true}
        hideTopBar={false}
        emptyText="No schema defined"
        defaultExpandedDepth={1}
        renderRootTreeLines={true}
      />
    </MosaicProvider>
  </React.StrictMode>
);
