import { ref } from "vue";

export function highlightRows(textMappings, paragraphPosition) {
  textMappings.value
    .filter(
      (mapping) =>
        mapping.start <= paragraphPosition.endPosition &&
        mapping.end >= paragraphPosition.startPosition
    )
    .forEach((mapping) => {
      highlightNode(mapping.node);
    });
}

function highlightNode(node) {
  // highlight the entire node
  node.style.backgroundColor = "yellow";
}

export const pdfViewer = ref(null);
export const pdfRenderKey = ref(0);
