# Latex

Documenting useful packages

## References

References can be added to most entities e.g. sections, tables, listings, figures etc.

### label

To access references, the referenced entities need to provide unique labels.

    \label{sec:secname}

`sec:` ... this first part is usually a shorthand for the type of label e.g. `sec:` for a section label, `lst:` for a code listing label, `fig:` for a figure etc.
`secname` ... this name needs to be unique within the scope of the shorthand prefix.

#### Section label

    \section{Section title A} \label{sec:sec_A}

#### Figure label

    \usepackage{graphicx}
    \begin{figure}
      \includegraphics{figure_name_A.pdf}
      \label{fig:nameA}
    \end{figure}

### Reference use

Add a reference for a section:

    ~\ref{sec:secname}

## footnote

    \footnote{...text...}

## url

    \url{...text...}

## Inline code

    \texttt{...text...}

## Code listings

    \usepackage{listings}
    
    \begin{lstlisting}
      ...text...
    \end{lstlisting}

