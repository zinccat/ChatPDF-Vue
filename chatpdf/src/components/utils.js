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

export const performRequestWithExponentialBackoff = async (
  requestFn,
  maxRetries = 3,
  delay = 1000
) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await requestFn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise((resolve) => setTimeout(resolve, delay));
      delay *= 2; // Double the delay for exponential backoff
    }
  }
};

export const pdfViewer = ref(null);
export const pdfRenderKey = ref(0);
