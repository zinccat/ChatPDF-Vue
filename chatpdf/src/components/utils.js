import { ref } from "vue";
import axios from "axios";

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


// Search text within the PDF and interact with a backend service
export const performSearch = async () => {
  if (!searchQuery.value || !pdfViewer.value) {
      console.error('Search query or PDF viewer not available')
      return
  }
  const textLayers = pdfViewer.value.querySelectorAll('.textLayer')
  const { combinedText, textMappings } = combineTextAndMap(textLayers)

  // eslint-disable-next-line no-unused-vars
  const sendRequest = async () => {
      return axios.post('http://localhost:5005/process_text', { text: combinedText, query: searchQuery.value })
  }
  
  try {
      console.log('sendRequest')
      const response = await performRequestWithExponentialBackoff(sendRequest)
      console.log(response.data.highlight)
      const paragraphPosition = findParagraphPosition(combinedText, response.data.highlight)
      console.log(paragraphPosition)
      if (paragraphPosition.startPosition === -1) {
          console.error('Highlight not found in combined text')
          return
      }
      highlightRows(textMappings, paragraphPosition)
  } catch (error) {
      console.error('Error:', error)
  }
}

// Process highlight response from backend
function findParagraphPosition(combinedText, paragraph) {
  const startPosition = combinedText.indexOf(paragraph)
  return { startPosition, endPosition: startPosition + paragraph.length - 1 }
}

export const pdfViewer = ref(null);
export const pdfRenderKey = ref(0);
export const textMappings = ref([]);
export const searchQuery = ref("")
