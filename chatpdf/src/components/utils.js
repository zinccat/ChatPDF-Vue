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

// Combine text from PDF text layers and map each text's position
export const combineTextAndMap = (textLayers) => {
  let combinedText = ''
  textMappings.value = []
  textLayers.forEach((layer) => {
      Array.from(layer.childNodes).forEach(node => {
          if (node.nodeType === Node.ELEMENT_NODE) {
              const nodeText = getNodeText(node).trim() + ' '
              const start = combinedText.length
              combinedText += nodeText
              textMappings.value.push({ start, end: start + nodeText.length - 1, node })
          }
      })
  })
  return { combinedText, textMappings }
}

const getNodeText = (node) => node.nodeType === Node.TEXT_NODE ? node.nodeValue :
  node.nodeType === Node.ELEMENT_NODE ? Array.from(node.childNodes).map(getNodeText).join(' ') : ''


export const pdfViewer = ref(null);
export const pdfRenderKey = ref(0);
export const textMappings = ref([]);
